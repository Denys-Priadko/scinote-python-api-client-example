"""
Template: Export Project Data
Description: Exports complete project structure including experiments, tasks, and results
Prerequisites: Valid API credentials, Team ID, Project ID
API Endpoints: Multiple (hierarchical data retrieval)
"""

# ===== CONFIGURATION =====
TEAM_ID = 1
PROJECT_ID = 1
OUTPUT_FILE = "project_export.json"  # Output file name
INCLUDE_RESULTS = True  # Whether to fetch results for each task
# =========================


# ============================================================================
# Auto-discovery: Find scinote_api.py by searching upward
# ============================================================================
# This allows you to run the script from anywhere - it will search for
# scinote_api.py in the current directory and all parent directories.
# Works in both script mode and interactive mode (IPython/Jupyter).
# ============================================================================

import sys
import json
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


print(f"\n{'=' * 70}")
print(f"Exporting Project {PROJECT_ID}")
print(f"{'=' * 70}\n")

# Step 1: Get project details
print("1. Fetching project details...")
project_response = api_request("GET", f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}")
project = project_response["data"]
project_data = {
    "id": project["id"],
    "name": project["attributes"].get("name", "N/A"),
    "description": project["attributes"].get("description", ""),
    "visibility": project["attributes"].get("visibility", "N/A"),
    "experiments": [],
}
print(f"   ✓ Project: {project_data['name']}")

# Step 2: Get all experiments in project
print("2. Fetching experiments...")
experiments_response = api_request(
    "GET", f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments"
)
experiments = experiments_response["data"]
print(f"   ✓ Found {len(experiments)} experiment(s)")

# Step 3: For each experiment, get tasks
for exp in experiments:
    exp_id = exp["id"]
    exp_attrs = exp["attributes"]

    experiment_data = {
        "id": exp_id,
        "name": exp_attrs.get("name", "N/A"),
        "description": exp_attrs.get("description", ""),
        "status": exp_attrs.get("status", "N/A"),
        "tasks": [],
    }

    print(f"\n   Experiment {exp_id}: {experiment_data['name']}")
    print(f"   ├─ Fetching tasks...")

    # Get tasks for this experiment
    tasks_response = api_request(
        "GET",
        f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{exp_id}/tasks",
    )
    tasks = tasks_response["data"]
    print(f"   │  ✓ Found {len(tasks)} task(s)")

    # Step 4: For each task, optionally get results
    for task in tasks:
        task_id = task["id"]
        task_attrs = task["attributes"]

        task_data = {
            "id": task_id,
            "name": task_attrs.get("name", "N/A"),
            "description": task_attrs.get("description", ""),
            "state": task_attrs.get("state", "N/A"),
            "status_name": task_attrs.get("status_name", "N/A"),
        }

        # Optionally fetch results
        if INCLUDE_RESULTS:
            try:
                results_response = api_request(
                    "GET",
                    f"/api/v1/teams/{TEAM_ID}/projects/{PROJECT_ID}/experiments/{exp_id}/tasks/{task_id}/results",
                )
                results = results_response["data"]

                task_data["results"] = [
                    {
                        "id": r["id"],
                        "name": r["attributes"].get("name", "N/A"),
                        "created_at": r["attributes"].get("created_at", "N/A"),
                    }
                    for r in results
                ]
                print(
                    f"   │  ├─ Task {task_id}: {task_data['name']} ({len(results)} results)"
                )
            except Exception as e:
                print(
                    f"   │  ├─ Task {task_id}: {task_data['name']} (error fetching results)"
                )
                task_data["results"] = []
        else:
            print(f"   │  ├─ Task {task_id}: {task_data['name']}")

        experiment_data["tasks"].append(task_data)

    project_data["experiments"].append(experiment_data)

# Step 5: Save to JSON file
print(f"\n3. Saving to {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(project_data, f, indent=2, ensure_ascii=False)

print(f"   ✓ Export saved")

# Summary
print(f"\n{'=' * 70}")
print(f"Export Complete!")
print(f"{'=' * 70}\n")

total_tasks = sum(len(exp["tasks"]) for exp in project_data["experiments"])
print(f"Summary:")
print(f"  - Project: {project_data['name']}")
print(f"  - Experiments: {len(project_data['experiments'])}")
print(f"  - Total Tasks: {total_tasks}")

if INCLUDE_RESULTS:
    total_results = sum(
        len(task.get("results", []))
        for exp in project_data["experiments"]
        for task in exp["tasks"]
    )
    print(f"  - Total Results: {total_results}")

print(f"\n  Output File: {OUTPUT_FILE}")
print(f"\n{'=' * 70}\n")
