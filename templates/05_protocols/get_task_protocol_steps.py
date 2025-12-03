"""
Template: Get Task Protocol Details
Description: Retrieves details and steps from a specific task protocol
Prerequisites: Valid API credentials, Team/Project/Experiment/Task/Protocol IDs
API Endpoint: GET /api/v1/teams/{team_id}/projects/{project_id}/experiments/{experiment_id}/tasks/{task_id}/protocols/{protocol_id}
Note: Use include=protocol_steps parameter to get steps in the response
"""

# ===== CONFIGURATION =====
TEAM_ID = 1           # Your team ID
PROJECT_ID = 5        # Your project ID
EXPERIMENT_ID = 10    # Your experiment ID
TASK_ID = 20          # Your task ID
PROTOCOL_ID = 1       # Protocol ID (use list_protocol_templates.py to find it)
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
# Note: Use ?include=protocol_steps to get steps in the response
endpoint = f'/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{EXPERIMENT_ID}/tasks/{TASK_ID}/protocols/{PROTOCOL_ID}?include=protocol_steps'
response = api_request('GET', endpoint)

# Display protocol details
protocol = response["data"]
attrs = protocol["attributes"]

print(f"\n{'=' * 70}")
print(f"Protocol Details - ID: {protocol['id']}")
print(f"{'=' * 70}\n")

print(f"Name: {attrs.get('name', 'N/A')}")
print(f"Description: {attrs.get('description', 'N/A')}")
print(f"Version: {attrs.get('version_number', 'N/A')}")

# Display protocol steps
print(f"\n{'=' * 70}")
print(f"Protocol Steps")
print(f"{'=' * 70}\n")

if "included" in response:
    steps = [item for item in response["included"] if item["type"] == "protocol_steps"]

    if steps:
        print(f"Found {len(steps)} step(s):\n")

        for step in sorted(steps, key=lambda s: s["attributes"].get("position", 0)):
            step_id = step["id"]
            step_attrs = step["attributes"]
            position = step_attrs.get("position", "N/A")
            name = step_attrs.get("name", "Unnamed Step")

            print(f"Step {position}: {name}")
            print(f"  Step ID: {step_id}")

            # Check if step has description/content
            if step_attrs.get("description"):
                desc = step_attrs.get("description", "")
                # Truncate long descriptions
                if len(desc) > 100:
                    desc = desc[:100] + "..."
                print(f"  Description: {desc}")

            print()
    else:
        print("No steps found for this protocol.")
else:
    print("No included data returned. Protocol may have no steps.")

print(f"{'=' * 70}\n")
