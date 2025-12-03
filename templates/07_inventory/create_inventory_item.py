"""
Template: Create Inventory Item
Description: Adds a new item to an inventory
Prerequisites: Valid API credentials, Team/Inventory IDs, API write permissions
API Endpoint: POST /api/v1/teams/{team_id}/inventories/{inventory_id}/items
"""


# ===== CONFIGURATION =====
TEAM_ID = 2
INVENTORY_ID = 1
ITEM_NAME = "Sample Reagent"  # Name of the new item
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
request_data = {"data": {"type": "inventory_items", "attributes": {"name": ITEM_NAME}}}

# Make the API request
endpoint = f"/api/v1/teams/{TEAM_ID}/inventories/{INVENTORY_ID}/items"
response = api_request("POST", endpoint, json_data=request_data)

# Display results
item = response["data"]
attrs = item["attributes"]
item_id = item["id"]

print(f"\n{'=' * 70}")
print(f"✓ Inventory Item Created Successfully!")
print(f"{'=' * 70}\n")

print(f"Item ID: {item_id}")
print(f"Name: {attrs.get('name', 'N/A')}")

print(f"\n{'=' * 70}\n")
print(f"💡 You can now update this item with additional data (custom columns).")
print()
