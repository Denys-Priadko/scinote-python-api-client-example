"""
Template: Create a New Project
Description: Creates a new project in a specified team
Prerequisites: Valid API credentials, Team ID, API write permissions
API Endpoint: POST /api/v1/teams/{team_id}/projects
"""


# ===== CONFIGURATION =====
TEAM_ID = 1                          # Replace with your team ID
PROJECT_NAME = "API Test Project"     # Name for the new project
PROJECT_VISIBILITY = "visible"        # Options: "visible" or "hidden"
# =========================


# ============================================================================
# Auto-discovery: Find scinote_api.py by searching upward
# ============================================================================
# This allows you to run the script from anywhere - it will search for
# scinote_api.py in the current directory and all parent directories.
# Works in both script mode and interactive mode (IPython/Jupyter).
# ============================================================================

import sys
from pathlib import Path

def find_api_module():
    """Search for scinote_api.py starting from current directory, then upward."""
    # Start from script location if running as script, otherwise from cwd
    if '__file__' in globals():
        search_start = Path(__file__).resolve().parent
    else:
        search_start = Path.cwd()

    # Search upward through parent directories
    current = search_start
    while current != current.parent:  # Stop at filesystem root
        if (current / 'scinote_api.py').exists():
            return current
        current = current.parent

    # Not found
    return None

api_location = find_api_module()
if api_location:
    sys.path.insert(0, str(api_location))
else:
    print("ERROR: Cannot find scinote_api.py")
    print("Make sure you're running this script from within the repository directory.")
    sys.exit(1)

from scinote_api import api_request
# ============================================================================


# Prepare the request data (JSON:API format)
request_data = {
    'data': {
        'type': 'projects',
        'attributes': {
            'name': PROJECT_NAME,
            'visibility': PROJECT_VISIBILITY
        }
    }
}

# Make the API request
response = api_request('POST', f'/api/v1/teams/{TEAM_ID}/projects',
                      json_data=request_data)

# Extract created project info
project = response['data']
project_id = project['id']
attrs = project['attributes']
name = attrs.get('name', 'N/A')

# Display results
print(f"\n{'='*70}")
print(f"✓ Project Created Successfully!")
print(f"{'='*70}\n")

print(f"Project ID: {project_id}")
print(f"Name: {name}")
print(f"Visibility: {attrs.get('visibility', 'N/A')}")
print(f"\n{'='*70}\n")

print(f"💡 Next steps:")
print(f"   - Use Project ID '{project_id}' in experiment templates")
print(f"   - View it in SciNote web interface under Team {TEAM_ID}")
print()
