"""
Template: Batch Create Projects
Description: Creates multiple projects from a list
Prerequisites: Valid API credentials, Team ID, API write permissions
API Endpoints: POST /api/v1/teams/{team_id}/projects (called multiple times)
"""


# ===== CONFIGURATION =====
TEAM_ID = 1

# List of project names to create
PROJECT_NAMES = [
    "Q1 2025 Experiments",
    "Q2 2025 Experiments",
    "Q3 2025 Experiments",
    "Q4 2025 Experiments"
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


print(f"\n{'='*70}")
print(f"Batch Creating {len(PROJECT_NAMES)} Projects")
print(f"{'='*70}\n")

created_projects = []

for project_name in PROJECT_NAMES:
    print(f"Creating: {project_name}...")

    request_data = {
        'data': {
            'type': 'projects',
            'attributes': {
                'name': project_name,
                'visibility': 'visible'
            }
        }
    }

    try:
        response = api_request('POST', f'/api/v1/teams/{TEAM_ID}/projects',
                              json_data=request_data)

        project_id = response['data']['id']
        created_projects.append({'id': project_id, 'name': project_name})
        print(f"  ✓ Created (ID: {project_id})")

    except Exception as e:
        print(f"  ✗ Failed: {str(e)[:100]}")

    print()

# Summary
print(f"{'='*70}")
print(f"Batch Creation Complete")
print(f"{'='*70}\n")

print(f"Successfully created {len(created_projects)} out of {len(PROJECT_NAMES)} projects:\n")
for proj in created_projects:
    print(f"  [{proj['id']}] {proj['name']}")

print(f"\n{'='*70}\n")
