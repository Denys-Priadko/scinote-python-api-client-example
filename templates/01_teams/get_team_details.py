"""
Template: Get Team Details
Description: Retrieves detailed information about a specific team
Prerequisites: Valid API credentials, Team ID
API Endpoint: GET /api/v1/teams/{id}
"""


# ===== CONFIGURATION =====
TEAM_ID = 3  # Replace with your team ID (run list_teams.py to find it)
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


# Make the API request
response = api_request("GET", f"/api/v1/teams/{TEAM_ID}")

# Extract team data
team = response["data"]
attrs = team["attributes"]

# Display results
print(f"\n{'=' * 70}")
print(f"Team Details - ID: {team['id']}")
print(f"{'=' * 70}\n")

print(f"Name: {attrs.get('name', 'N/A')}")
print(f"Description: {attrs.get('description', '(No description)')}")
space_taken = attrs.get('space_taken', 0)
print(f"Storage Used: {space_taken / (1024 * 1024):.2f} MB")
print(f"Created: {attrs.get('created_at', 'N/A')}")
print(f"Updated: {attrs.get('updated_at', 'N/A')}")

print(f"\n{'=' * 70}\n")
