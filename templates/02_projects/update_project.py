"""
Template: Update Project Information
Description: Updates the name or visibility of an existing project
Prerequisites: Valid API credentials, Team ID, Project ID, API write permissions
API Endpoint: PATCH /api/v1/teams/{team_id}/projects/{project_id}
"""

# ===== CONFIGURATION =====
TEAM_ID = 2  # Your team ID
PROJECT_ID = 2  # Project to update
NEW_PROJECT_NAME = "Updated Project"  # New name (or keep original if unchanged)
NEW_VISIBILITY = "visible"  # Options: "visible" or "hidden"
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
    if "__file__" in globals():
        search_start = Path(__file__).resolve().parent
    else:
        search_start = Path.cwd()

    # Search upward through parent directories
    current = search_start
    while current != current.parent:  # Stop at filesystem root
        if (current / "scinote_api.py").exists():
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


# Prepare the request data
request_data = {
    "data": {
        "type": "projects",
        "attributes": {"name": NEW_PROJECT_NAME, "visibility": NEW_VISIBILITY},
    }
}

# Make the API request
response = api_request(
    "PATCH", f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}", json_data=request_data
)

# Display results
print(f"\n{'=' * 70}")
print(f"✓ Project Updated Successfully!")
print(f"{'=' * 70}\n")

# Check if server returned full data or just success (when nothing changed)
if "data" in response:
    project = response["data"]
    attrs = project["attributes"]
    print(f"Project ID: {project['id']}")
    print(f"New Name: {attrs.get('name', 'N/A')}")
    print(f"Visibility: {attrs.get('visibility', 'N/A')}")
else:
    # Server returned 204 No Content (project unchanged)
    print(f"Project ID: {PROJECT_ID}")
    print(f"Note: No changes detected - project already has the specified values")

print(f"\n{'=' * 70}\n")
