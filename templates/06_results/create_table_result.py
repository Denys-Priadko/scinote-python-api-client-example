"""
Template: Create Table Result
Description: Creates a table-based result for a task
Prerequisites: Valid API credentials, IDs, API write permissions
API Endpoint: POST /api/v1/teams/{team_id}/projects/{project_id}/experiments/{experiment_id}/tasks/{task_id}/results
"""

# ===== CONFIGURATION =====
TEAM_ID = 1
PROJECT_ID = 1
EXPERIMENT_ID = 1
TASK_ID = 2

RESULT_NAME = "Measurement Data"

# Table structure: Define columns and rows
# Format: 2D array where first row is headers
TABLE_DATA = [
    ["Sample ID", "Temperature (°C)", "pH", "Concentration (mg/L)"],
    ["Sample-001", "25.3", "7.2", "12.5"],
    ["Sample-002", "26.1", "7.4", "13.8"],
    ["Sample-003", "24.8", "7.1", "11.9"],
]
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


# Convert table data to JSON structure expected by API
# The API expects contents as a 2D JSON array
table_contents = TABLE_DATA

# Prepare request data
request_data = {
    "data": {"type": "results", "attributes": {"name": RESULT_NAME}},
    "included": [{"type": "result_tables", "attributes": {"contents": table_contents}}],
}

# Make the API request
endpoint = f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{EXPERIMENT_ID}/tasks/{TASK_ID}/results"
response = api_request("POST", endpoint, json_data=request_data)

# Display results
result = response["data"]
attrs = result["attributes"]
result_id = result["id"]

print(f"\n{'=' * 70}")
print(f"✓ Table Result Created Successfully!")
print(f"{'=' * 70}\n")

print(f"Result ID: {result_id}")
print(f"Name: {attrs.get('name', 'N/A')}")
print(f"Table Size: {len(TABLE_DATA)} rows × {len(TABLE_DATA[0])} columns")

print(f"\n{'=' * 70}\n")
print(f"💡 View this result in SciNote under Task {TASK_ID}")
print()
