"""
Template: List All Teams
Description: Retrieves and displays all teams you have access to
Prerequisites: Valid API credentials
API Endpoint: GET /api/v1/teams
"""


# ===== CONFIGURATION =====
# No configuration needed - lists all your teams
# =========================


# ============================================================================
# Auto-discovery: Find scinote_api.py by searching upward
# ============================================================================

import sys
from pathlib import Path


def find_api_module():
    """Search for scinote_api.py starting from current directory, then upward."""
    if '__file__' in globals():
        search_start = Path(__file__).resolve().parent
    else:
        search_start = Path.cwd()

    current = search_start
    while current != current.parent:
        if (current / 'scinote_api.py').exists():
            return current
        current = current.parent
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
response = api_request('GET', '/api/v1/teams')

# Display results
print(f"\n{'='*70}")
print(f"Found {len(response['data'])} team(s)")
print(f"{'='*70}\n")

for team in response['data']:
    team_id = team['id']
    attrs = team['attributes']
    team_name = attrs.get('name', 'Unnamed Team')
    description = attrs.get('description', '')
    space_used = attrs.get('space_taken', 0) / (1024*1024)  # Convert to MB
    created_at = attrs.get('created_at', 'N/A')

    print(f"Team ID: {team_id}")
    print(f"  Name: {team_name}")
    if description:
        print(f"  Description: {description}")
    print(f"  Storage Used: {space_used:.2f} MB")
    print(f"  Created: {created_at}")
    print()

print(f"{'='*70}")
print(f"\n💡 Tip: Use a Team ID in other templates to work with that team's data.\n")
