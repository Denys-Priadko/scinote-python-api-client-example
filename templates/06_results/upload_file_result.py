"""
Template: Upload File as Result
Description: Uploads a file as a result for a task
Prerequisites: Valid API credentials, IDs, file to upload, API write permissions
API Endpoint: POST /api/v1/teams/{team_id}/projects/{project_id}/experiments/{experiment_id}/tasks/{task_id}/results
"""

# ===== CONFIGURATION =====
TEAM_ID = 1
PROJECT_ID = 1
EXPERIMENT_ID = 1
TASK_ID = 2

RESULT_NAME = "E. coli microscopy image"
FILE_PATH = "../../sample_data/ecoli.jpg"  # Path to file
FILE_TYPE = "image/jpeg"  # MIME type
FILE_NAME = "ecoli_result.jpg"  # Name for the uploaded file
# =========================


# ============================================================================
# Auto-discovery: Find scinote_api.py by searching upward
# ============================================================================
# This allows you to run the script from anywhere - it will search for
# scinote_api.py in the current directory and all parent directories.
# Works in both script mode and interactive mode (IPython/Jupyter).
# ============================================================================

import sys
import base64
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


# Read and encode the file as Base64
print("Reading file...")
with open(FILE_PATH, "rb") as f:
    file_content = f.read()
    b64_content = base64.b64encode(file_content).decode("ascii")

print(f"File size: {len(file_content)} bytes")

# Prepare request data
request_data = {
    "data": {"type": "results", "attributes": {"name": RESULT_NAME}},
    "included": [
        {
            "type": "result_files",
            "attributes": {
                "file_name": FILE_NAME,
                "file_type": FILE_TYPE,
                "file_data": b64_content,
            },
        }
    ],
}

# Make the API request
print("Uploading result...")
endpoint = f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{EXPERIMENT_ID}/tasks/{TASK_ID}/results"
response = api_request("POST", endpoint, json_data=request_data)

# Display results
result = response["data"]
attrs = result["attributes"]
result_id = result["id"]

print(f"\n{'=' * 70}")
print(f"✓ Result Uploaded Successfully!")
print(f"{'=' * 70}\n")

print(f"Result ID: {result_id}")
print(f"Name: {attrs.get('name', 'N/A')}")

print(f"\n{'=' * 70}\n")
print(f"💡 View this result in SciNote under Task {TASK_ID}")
print()
