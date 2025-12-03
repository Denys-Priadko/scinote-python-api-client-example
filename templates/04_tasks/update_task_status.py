"""
Template: Update Task Status
Description: Updates the status/state of a task (e.g., to mark it as complete)
Prerequisites: Valid API credentials, Team/Project/Experiment/Task IDs, API write permissions
API Endpoint: PATCH /api/v1/teams/{team_id}/projects/{project_id}/experiments/{experiment_id}/tasks/{task_id}
Note: Use list_tasks.py to see current status and available status IDs
"""


# ===== CONFIGURATION =====
TEAM_ID = 1                      # Your team ID
PROJECT_ID = 5                   # Your project ID
EXPERIMENT_ID = 10               # Your experiment ID
TASK_ID = 20                     # Task to update
NEW_STATUS_ID = 2                # New status ID (use list_tasks.py to find valid IDs)
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


# Prepare request data
request_data = {
    'data': {
        'type': 'tasks',
        'attributes': {
            'status_id': NEW_STATUS_ID
        }
    }
}

# Make the API request
endpoint = f'/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{EXPERIMENT_ID}/tasks/{TASK_ID}'
response = api_request('PATCH', endpoint, json_data=request_data)

# Display results
print(f"\n{'='*70}")
print(f"✓ Task Status Updated Successfully!")
print(f"{'='*70}\n")

# Check if server returned full data or just success (when nothing changed)
if 'data' in response:
    task = response['data']
    attrs = task['attributes']
    print(f"Task ID: {task['id']}")
    print(f"Name: {attrs.get('name', 'N/A')}")
    print(f"Current Status ID: {attrs.get('status_id', 'N/A')}")
    print(f"Status Name: {attrs.get('status_name', 'N/A')}")
    print(f"State: {attrs.get('state', 'N/A')}")

    print(f"\n{'='*70}")
    print(f"\n💡 Tip: Use list_tasks.py to see available status transitions:")
    print(f"   - next_status_id: {attrs.get('next_status_id', 'N/A')}")
    print(f"   - next_status_name: {attrs.get('next_status_name', 'N/A')}")
else:
    # Server returned 204 No Content (task unchanged)
    print(f"Task ID: {TASK_ID}")
    print(f"Note: No changes detected - task already has the specified status")
    print(f"\n{'='*70}")

print()
