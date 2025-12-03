"""
Template: Update Inventory Item
Description: Updates the name or attributes of an existing inventory item
Prerequisites: Valid API credentials, Team/Inventory/Item IDs, API write permissions
API Endpoint: PATCH /api/v1/teams/{team_id}/inventories/{inventory_id}/items/{item_id}
"""

# ===== CONFIGURATION =====
TEAM_ID = 2
INVENTORY_ID = 1
ITEM_ID = 2  # Item to update
NEW_ITEM_NAME = "Updated Reagent Name"  # New name for the item
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
    "data": {
        "type": "inventory_items",
        "id": str(ITEM_ID),  # Required by inventory items controller
        "attributes": {"name": NEW_ITEM_NAME}
    }
}

# Make the API request
endpoint = f"/api/v1/teams/{TEAM_ID}/inventories/{INVENTORY_ID}/items/{ITEM_ID}"
response = api_request("PATCH", endpoint, json_data=request_data)

# Display results
print(f"\n{'=' * 70}")
print(f"✓ Inventory Item Updated Successfully!")
print(f"{'=' * 70}\n")

# Check if server returned full data or just success (when nothing changed)
if "data" in response:
    item = response["data"]
    attrs = item["attributes"]
    print(f"Item ID: {item['id']}")
    print(f"New Name: {attrs.get('name', 'N/A')}")
else:
    # Server returned 204 No Content (item unchanged)
    print(f"Item ID: {ITEM_ID}")
    print(f"Note: No changes detected - item already has the specified values")

print(f"\n{'=' * 70}\n")
print(f"💡 To update custom column values, use the inventory cells endpoints")
print(f"   (requires knowledge of column IDs and cell structure)")
print()
