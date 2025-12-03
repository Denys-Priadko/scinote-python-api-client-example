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
