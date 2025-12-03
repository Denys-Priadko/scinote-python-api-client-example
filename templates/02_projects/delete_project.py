"""
Template: Archive (Delete) a Project
Description: Archives an existing project by setting archived=true
Prerequisites: Valid API credentials, Team ID, Project ID, API write permissions
API Endpoint: PATCH /api/v1/teams/{team_id}/projects/{project_id}
Note: SciNote uses archiving instead of hard deletion to preserve data
"""


# ===== CONFIGURATION =====
TEAM_ID = 1         # Your team ID
PROJECT_ID = 5      # Project to archive
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


# Prepare the request data (set archived to true)
request_data = {
    "data": {
        "type": "projects",
        "attributes": {"archived": True},
    }
}

# Make the API request
response = api_request(
    "PATCH", f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}", json_data=request_data
)

# Display results
project = response["data"]
attrs = project["attributes"]

print(f"\n{'=' * 70}")
print(f"✓ Project Archived Successfully!")
print(f"{'=' * 70}\n")

print(f"Project ID: {project['id']}")
print(f"Name: {attrs.get('name', 'N/A')}")
print(f"Archived: {attrs.get('archived', False)}")

print(f"\n{'=' * 70}")
print(f"\n💡 Archived projects can be restored by setting archived=false")
print(f"   Use update_project.py and set the archived attribute to False.\n")
