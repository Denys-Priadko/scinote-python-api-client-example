# SciNote API Examples - Python Client

Welcome! This repository contains ready-to-use Python examples for interacting with the SciNote@UBT API.

**Full API reference:** [SciNote API Documentation](https://scinote-eln.github.io/scinote-api-docs/) (we're using V1)

## What You Can Do

The SciNote API lets you automate your laboratory workflows:

- **Manage projects and experiments** - Create, update, organize
- **Work with protocols** - Access templates, add steps
- **Record results** - Upload files, tables, measurements
- **Track inventory** - Manage laboratory resources
- **Generate reports** - Export experimental data
- **...and much more!**

## Quick Start (2 Steps!)

### 1. Download Your API Credentials

1. Log in to SciNote@UBT web interface
2. Click **"Automate with API"** in the left sidebar menu
3. Click the **"Generate Credentials"** button
4. Save the downloaded file (e.g., `api_credentials_2025-12-03T102351.json`) in this directory

**That's it!** The credential file contains everything needed to authenticate.

**Please keep your credentials secret!**

### 2. Run Any Example

```bash
# List all your teams
python3 templates/01_teams/list_teams.py

# Create a new project
python3 templates/02_projects/create_project.py

# Upload a result file
python3 templates/06_results/upload_file_result.py
```

The examples automatically:

- ✓ Find your credential file
- ✓ Refresh tokens when expired
- ✓ Handle authentication
- ✓ Show clear error messages

## Template Library

All examples are in the `templates/` directory, organized by category:

### Teams & Users

- `01_teams/list_teams.py` - List all teams you belong to
- `01_teams/get_team_details.py` - Get details about a specific team

### Projects

- `02_projects/list_projects.py` - List projects in a team
- `02_projects/create_project.py` - Create a new project
- `02_projects/update_project.py` - Update project information
- `02_projects/delete_project.py` - Archive a project

### Experiments

- `03_experiments/list_experiments.py` - List experiments in a project
- `03_experiments/create_experiment.py` - Create a new experiment
- `03_experiments/update_experiment.py` - Update experiment information

### Tasks

- `04_tasks/list_tasks.py` - List tasks (my_modules) in an experiment
- `04_tasks/create_task.py` - Create a new task
- `04_tasks/update_task_status.py` - Update task status

### Protocols

get_task_protocol_steps.py
/023 󰌠 list_task_protocols.py

- `05_protocols/get_task_protocol_steps.py` - List task protocol steps
- `05_protocols/list_task_protocols.py` - Get steps from a task protocol

### Results

- `06_results/list_results.py` - List results for a task
- `06_results/upload_file_result.py` - Upload a file as a result
- `06_results/create_text_result.py` - Create a text result
- `06_results/create_table_result.py` - Create a table result

### Inventory

- `07_inventory/list_inventories.py` - List all inventories in a team
- `07_inventory/list_inventory_items.py` - List items in an inventory
- `07_inventory/create_inventory_item.py` - Add a new inventory item
- `07_inventory/update_inventory_item.py` - Update an existing item

### Advanced

- `08_advanced/batch_create_projects.py` - Create multiple projects from a list
- `08_advanced/export_project_data.py` - Export complete project structure

## How to Use Templates

These templates are meant to get you started and provide boilerplate code for the atomic API actions. While you can use the templates for both learning and for actual work, the real power of API lies in writing your own scripts that use multiple API actions.

Each template is a standalone script with clear configuration at the top:

```python
"""
Template: Create a New Project
Description: Creates a project in a specified team
"""

# ===== CONFIGURATION =====
TEAM_ID = 1              # Replace with your team ID
PROJECT_NAME = "My New Project"
PROJECT_DESCRIPTION = "Created via API"
# =========================

from scinote_api import api_request

response = api_request('POST', f'/api/v1/teams/{TEAM_ID}/projects',
                      json_data={'data': {
                          'type': 'projects',
                          'attributes': {
                              'name': PROJECT_NAME,
                              'description': PROJECT_DESCRIPTION
                          }
                      }})

print(f"✓ Created project: {response['data']['attributes']['name']}")
print(f"  Project ID: {response['data']['id']}")
```

**To customize:**

1. Edit values in the `CONFIGURATION` section
2. Run the script: `python3 template_name.py`
3. See the results!

## API Write Permissions

**Important:** Creating, modifying, or deleting data requires API write permission.

### Who Can Write via API?

1. **Team Administrators** - Always have full API write access
2. **Regular Team Members** - Need explicit permission from a team administrator

**Happy Automating!**
