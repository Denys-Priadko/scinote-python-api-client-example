"""
Template: Create Text Result
Description: Creates a text-based result for a task
Prerequisites: Valid API credentials, IDs, API write permissions
API Endpoint: POST /api/v1/teams/{team_id}/projects/{project_id}/experiments/{experiment_id}/tasks/{task_id}/results
"""

# ===== CONFIGURATION =====
TEAM_ID = 1
PROJECT_ID = 1
EXPERIMENT_ID = 1
TASK_ID = 2

RESULT_NAME = "Experimental Observations"
TEXT_CONTENT = """
<p>Sample was analyzed under microscope at 400x magnification.</p>
<p><strong>Observations:</strong></p>
<ul>
  <li>Cell morphology appears normal</li>
  <li>No contamination detected</li>
  <li>Growth rate is within expected range</li>
</ul>
<p><em>Conclusion: Sample is suitable for further analysis.</em></p>
"""
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
    "data": {"type": "results", "attributes": {"name": RESULT_NAME}},
    "included": [{"type": "result_texts", "attributes": {"text": TEXT_CONTENT}}],
}

# Make the API request
endpoint = f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{EXPERIMENT_ID}/tasks/{TASK_ID}/results"
response = api_request("POST", endpoint, json_data=request_data)

# Display results
result = response["data"]
attrs = result["attributes"]
result_id = result["id"]

print(f"\n{'=' * 70}")
print(f"✓ Text Result Created Successfully!")
print(f"{'=' * 70}\n")

print(f"Result ID: {result_id}")
print(f"Name: {attrs.get('name', 'N/A')}")

print(f"\n{'=' * 70}\n")
print(f"💡 View this result in SciNote under Task {TASK_ID}")
print()
