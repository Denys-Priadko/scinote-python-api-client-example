"""
Template: List Items in an Inventory
Description: Retrieves all items from a specified inventory
Prerequisites: Valid API credentials, Team ID, Inventory ID
API Endpoint: GET /api/v1/teams/{team_id}/inventories/{inventory_id}/items
"""

# ===== CONFIGURATION =====
TEAM_ID = 2  # Your team ID
INVENTORY_ID = 1  # Your inventory ID
PAGE_SIZE = 25  # Number of items per page (optional, max 100)
PAGE_NUMBER = 1  # Which page to retrieve (starts at 1)
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
# Note: Pagination is done via query parameters in the URL
# Use links.next from response to get subsequent pages
endpoint = f"/api/v1/teams/{TEAM_ID}/inventories/{INVENTORY_ID}/items?page[size]={PAGE_SIZE}&page[number]={PAGE_NUMBER}"
response = api_request("GET", endpoint)

# Display results
print(f"\n{'=' * 70}")
print(f"Items in Inventory {INVENTORY_ID}")
print(f"Found {len(response['data'])} item(s)")
print(f"{'=' * 70}\n")

for item in response["data"]:
    item_id = item["id"]
    attrs = item["attributes"]
    name = attrs.get("name", "N/A")
    created = attrs.get("created_at", "N/A")

    print(f"Item ID: {item_id}")
    print(f"  Name: {name}")
    print(f"  Created: {created}")
    print()

print(f"{'=' * 70}")

# Check if there are more pages
if "links" in response and "next" in response["links"] and response["links"]["next"]:
    print(
        f"\n💡 There are more items. To get the next page, set PAGE_NUMBER = {PAGE_NUMBER + 1}"
    )
    print(f"   Or use the next link: {response['links']['next']}\n")
else:
    print(f"\n✓ All items retrieved (no more pages).\n")
