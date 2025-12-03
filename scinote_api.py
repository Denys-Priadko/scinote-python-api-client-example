"""
SciNote API Client - Simplified Authentication & Request Handling

This module provides a simple api_request() function that automatically handles:
- Finding credential files
- Token refresh when expired
- Clear error messages for debugging

Usage:
    from scinote_api import api_request

    # GET request
    teams = api_request('GET', '/api/v1/teams')

    # POST request with JSON
    project = api_request('POST', f'/api/v1/teams/{team_id}/projects',
                          json={'data': {'type': 'projects',
                                        'attributes': {'name': 'New Project'}}})
"""

import json
import time
import glob
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# === Error Message Mappings ===

HTTP_ERROR_GUIDANCE = {
    400: (
        "Bad Request - The server couldn't understand your request.\n"
        "→ Check if your data is formatted correctly according to the API docs.\n"
        "→ Common issue: Missing required fields or wrong data types."
    ),
    401: (
        "Authentication Failed - Your credentials are invalid or expired.\n"
        "→ Download fresh credentials from SciNote: 'Automate with API' menu → 'Generate Credentials'.\n"
        "→ Make sure the credential file is in the same directory as your script."
    ),
    # 403 is handled dynamically in _handle_api_error() based on HTTP method
    404: (
        "Resource Not Found - The requested item doesn't exist.\n"
        "→ Check if the IDs in your request URL are correct.\n"
        "→ Example: Team ID, Project ID, Experiment ID, Task ID, etc."
    ),
    422: (
        "Invalid Data - The server couldn't process your request.\n"
        "→ Check the response details below for specific validation errors.\n"
        "→ Common issue: Required fields missing or data constraints violated."
    ),
    500: (
        "Server Error - Something went wrong on the SciNote server.\n"
        "→ This is not your fault. Try again in a few moments.\n"
        "→ If it persists, contact SciNote support."
    ),
    503: (
        "Service Unavailable - The SciNote server is temporarily down.\n"
        "→ The server may be undergoing maintenance.\n"
        "→ Try again in a few minutes."
    )
}


def _find_credential_file():
    """
    Find the most recent API credential file.

    Looks for files matching pattern: api_credentials_*.json
    Checks both current directory and parent directory (for scripts in subdirs).
    Returns the newest file by filename timestamp.

    Returns:
        Path: Path to the credential file

    Raises:
        FileNotFoundError: If no credential files found
    """
    # Check current directory first
    credential_files = glob.glob('api_credentials_*.json')

    # If not found, check parent directory (for scripts in templates/ subdirs)
    if not credential_files:
        credential_files = glob.glob('../api_credentials_*.json')

    # If still not found, check two levels up (for deeply nested templates)
    if not credential_files:
        credential_files = glob.glob('../../api_credentials_*.json')

    assert credential_files, (
        "No credential files found!\n\n"
        "→ Download your API credentials from SciNote:\n"
        "  1. Open SciNote web interface\n"
        "  2. Click 'Automate with API' in the left menu\n"
        "  3. Click 'Generate Credentials' button\n"
        "  4. Save the downloaded file in this directory\n\n"
        "The file should be named like: api_credentials_2025-12-03T102351.json"
    )

    # Sort by filename (includes timestamp) and return the newest
    credential_files.sort()
    latest_file = credential_files[-1]

    print(f"Using credentials: {os.path.basename(latest_file)}")
    return Path(latest_file)


def _load_credentials():
    """Load credentials from the most recent credential file."""
    cred_file = _find_credential_file()

    try:
        with open(cred_file, 'r') as f:
            credentials = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON in credential file: {cred_file}\n"
            f"Error: {e}\n"
            f"→ The file may be corrupted. Download a fresh copy from SciNote."
        )

    # Validate required fields
    required_fields = ['server_url', 'api_uid', 'api_secret', 'access_token', 'refresh_token']
    missing_fields = [f for f in required_fields if f not in credentials]
    assert not missing_fields, (
        f"Credential file is missing required fields: {', '.join(missing_fields)}\n"
        f"→ Download fresh credentials from SciNote."
    )

    return credentials, cred_file


def _refresh_token_if_needed(credentials, cred_file):
    """
    Check if access token has expired and refresh it if necessary.

    Updates the credential file with new tokens if refreshed.
    """
    # Check if token is expired (with 60 second buffer)
    token_created = credentials.get('access_token_created_at', 0)
    token_expires_in = credentials.get('access_token_expires_in', 7200)

    if token_created + token_expires_in > int(time.time()) + 60:
        # Token is still valid
        return credentials

    print("Access token expired, refreshing...")

    # Prepare refresh token request
    url = credentials['server_url'] + "/oauth/token"
    payload = json.dumps({
        'grant_type': 'refresh_token',
        'client_id': credentials['api_uid'],
        'client_secret': credentials['api_secret'],
        'redirect_uri': credentials.get('api_redirect_uri', 'urn:ietf:wg:oauth:2.0:oob'),
        'refresh_token': credentials['refresh_token']
    }).encode('utf-8')

    request = Request(url, data=payload, headers={
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    })

    try:
        response = urlopen(request)
        token_data = json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ''
        raise RuntimeError(
            "Failed to refresh access token.\n"
            f"Server response ({e.code}): {error_body}\n\n"
            "→ Your refresh token may have expired.\n"
            "→ Download new credentials from SciNote: 'Automate with API' menu."
        )
    except URLError as e:
        raise ConnectionError(
            f"Cannot connect to SciNote server: {credentials['server_url']}\n"
            f"Error: {e.reason}\n\n"
            "→ Check your internet connection\n"
            "→ Verify the server URL in your credentials file"
        )

    # Update credentials with new tokens
    credentials['access_token'] = token_data['access_token']
    credentials['refresh_token'] = token_data['refresh_token']
    credentials['access_token_created_at'] = token_data['created_at']
    credentials['access_token_expires_in'] = token_data['expires_in']

    # Save updated credentials back to file
    with open(cred_file, 'w') as f:
        json.dump(credentials, f, indent=2)

    print("✓ Token refreshed successfully")
    return credentials


def _handle_api_error(error, endpoint, method):
    """Format HTTP errors with helpful guidance for users."""
    error_code = error.code

    # Try to parse error body for details
    try:
        error_body = error.read().decode()
        error_json = json.loads(error_body)
        error_details = json.dumps(error_json, indent=2)
    except:
        error_details = error.read().decode() if error.fp else "No details available"

    # Get guidance message for this error code
    # Special handling for 403 based on HTTP method and resource scope
    if error_code == 403:
        # Determine if this is a read or write operation
        is_read_operation = method.upper() == 'GET'

        # Determine if this is a team-scoped or project-scoped resource
        # Project-scoped resources have /projects/{id} in their path
        is_project_scoped = '/projects/' in endpoint

        if is_read_operation:
            guidance = (
                "Permission Denied - You don't have access to this resource.\n"
                "→ Make sure you entered the correct resource ID under CONFIGURATION in the script.\n"
                "→ Verify that you have permission to access this resource.\n"
                "→ If you don't have the permission, ask the resource owner to give it to you."
            )
        elif is_project_scoped:
            # Project-scoped write operation (experiments, tasks, results, etc.)
            guidance = (
                "Permission Denied - You don't have API write access for this resource.\n"
                "→ You can only change data programmatically (via API) if:\n"
                "  • You are an administrator of the team that owns this project, OR\n"
                "  • A team administrator has given you project-level write permission.\n\n"
                "To get project-level write permission:\n"
                "  1. Ask a team administrator to open the project in SciNote\n"
                "  2. They go to: Project → User Management (team icon)\n"
                "  3. They find your user and enable: 'Can change data programmatically'\n\n"
                "Alternatively, contact the team owner to make you a team administrator."
            )
        else:
            # Team-scoped write operation (inventories, team settings, etc.)
            guidance = (
                "Permission Denied - You don't have permission to modify this team-level resource.\n"
                "→ Team-scoped resources (like inventories) can only be modified by team administrators.\n"
                "→ There is no project-level permission that grants access to these resources.\n\n"
                "To get access:\n"
                "  • Contact the team owner and ask them to make you a team administrator.\n"
                "  • Team administrators have full access to all team resources via API."
            )
    else:
        guidance = HTTP_ERROR_GUIDANCE.get(error_code,
            f"HTTP {error_code} error occurred. Check the API documentation for details."
        )

    # Format comprehensive error message
    error_message = (
        f"\n{'='*70}\n"
        f"API Request Failed: {method.upper()} {endpoint}\n"
        f"{'='*70}\n\n"
        f"Error Code: {error_code}\n\n"
        f"{guidance}\n\n"
        f"Server Response:\n{error_details}\n"
        f"{'='*70}\n"
    )

    raise RuntimeError(error_message)


def api_request(method, endpoint, json_data=None, **kwargs):
    """
    Make an authenticated API request to SciNote.

    Automatically handles:
    - Finding and loading credentials
    - Token refresh if expired
    - Authentication headers
    - Error handling with clear messages

    Args:
        method (str): HTTP method ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
        endpoint (str): API endpoint path (e.g., '/api/v1/teams')
        json_data (dict, optional): Data to send as JSON body
        **kwargs: Additional arguments passed to urllib.request.Request

    Returns:
        dict: Parsed JSON response from the API

    Examples:
        # List all teams
        teams = api_request('GET', '/api/v1/teams')

        # Create a project
        project = api_request('POST', f'/api/v1/teams/1/projects',
                             json_data={'data': {'type': 'projects',
                                                'attributes': {'name': 'My Project'}}})

        # Update a project
        project = api_request('PATCH', f'/api/v1/teams/1/projects/5',
                             json_data={'data': {'type': 'projects',
                                                'attributes': {'name': 'Updated Name'}}})
    """
    # Load and refresh credentials
    credentials, cred_file = _load_credentials()
    credentials = _refresh_token_if_needed(credentials, cred_file)

    # Build full URL
    url = credentials['server_url'] + endpoint

    # Prepare request
    headers = {
        'Authorization': f"Bearer {credentials['access_token']}",
        'Accept': 'application/json'
    }

    # Add JSON body if provided
    data = None
    if json_data is not None:
        headers['Content-Type'] = 'application/vnd.api+json'
        data = json.dumps(json_data).encode('utf-8')

    # Create request
    request = Request(url, data=data, headers=headers, method=method.upper())

    # Make request with error handling
    try:
        response = urlopen(request)
        response_body = response.read().decode()

        # Parse JSON response (if any)
        if response_body:
            return json.loads(response_body)
        else:
            return {'success': True}  # For DELETE requests with no body

    except HTTPError as e:
        _handle_api_error(e, endpoint, method)
    except URLError as e:
        raise ConnectionError(
            f"Cannot connect to SciNote server: {credentials['server_url']}\n"
            f"Error: {e.reason}\n\n"
            "→ Check your internet connection\n"
            "→ Verify the server URL is correct"
        )
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Server returned invalid JSON response.\n"
            f"Error: {e}\n"
            f"→ This might indicate a server error. Contact SciNote support."
        )
