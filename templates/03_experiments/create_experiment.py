"""
Template: Create a New Experiment
Description: Creates a new experiment in a specified project
Prerequisites: Valid API credentials, Team/Project IDs, API write permissions
API Endpoint: POST /api/v1/teams/{team_id}/projects/{project_id}/experiments
"""

# ===== CONFIGURATION =====
TEAM_ID = 1  # Your team ID
PROJECT_ID = 1  # Your project ID
EXPERIMENT_NAME = "API Test Experiment"  # Name for the new experiment
EXPERIMENT_DESCRIPTION = "Created via API"  # Optional description
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


# Prepare request data
request_data = {
    "data": {
        "type": "experiments",
        "attributes": {"name": EXPERIMENT_NAME, "description": EXPERIMENT_DESCRIPTION},
    }
}

# Make the API request
response = api_request(
    "POST",
    f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments",
    json_data=request_data,
)

# Display results
experiment = response["data"]
attrs = experiment["attributes"]
exp_id = experiment["id"]

print(f"\n{'=' * 70}")
print(f"✓ Experiment Created Successfully!")
print(f"{'=' * 70}\n")

print(f"Experiment ID: {exp_id}")
print(f"Name: {attrs.get('name', 'N/A')}")
print(f"Description: {attrs.get('description', 'N/A')}")

print(f"\n{'=' * 70}\n")
print(f"💡 Next steps:")
print(f"   - Use Experiment ID '{exp_id}' to create tasks")
print(f"   - View it in SciNote under Project {PROJECT_ID}")
print()
