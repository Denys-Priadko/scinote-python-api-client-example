"""
Template: List Tasks in an Experiment
Description: Retrieves all tasks (my_modules) in a specified experiment
Prerequisites: Valid API credentials, Team/Project/Experiment IDs
API Endpoint: GET /api/v1/teams/{team_id}/projects/{project_id}/experiments/{experiment_id}/tasks
"""

# ===== CONFIGURATION =====
TEAM_ID = 1  # Your team ID
PROJECT_ID = 1  # Your project ID
EXPERIMENT_ID = 4  # Your experiment ID
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
endpoint = (
    f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{EXPERIMENT_ID}/tasks"
)
response = api_request("GET", endpoint)

# Display results
print(f"\n{'=' * 70}")
print(f"Tasks in Experiment {EXPERIMENT_ID}")
print(f"Found {len(response['data'])} task(s)")
print(f"{'=' * 70}\n")

for task in response["data"]:
    task_id = task["id"]
    attrs = task["attributes"]
    name = attrs.get("name", "N/A")
    state = attrs.get("state", "N/A")
    started = attrs.get("started_on", "N/A")
    completed = attrs.get("completed_on", "N/A")

    # Format state indicator
    state_icon = {"uncompleted": "⭕", "in_progress": "🔄", "completed": "✓"}.get(
        state, "❓"
    )

    print(f"{state_icon} Task ID: {task_id}")
    print(f"   Name: {name}")
    print(f"   State: {state}")
    if started:
        print(f"   Started: {started}")
    if completed:
        print(f"   Completed: {completed}")
    print()

print(f"{'=' * 70}")
print(f"\n💡 Tip: Use a Task ID to add results, protocols, or inventory items.\n")
