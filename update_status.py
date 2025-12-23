"""
Status updater script called by Claude Code hooks
Writes current Claude status to a file for the monitor to read
"""

import sys
import json
from pathlib import Path
from datetime import datetime

STATUS_FILE = Path(__file__).parent / "claude_status.json"


def update_status(status, message=""):
    """Update the status file with current Claude state"""
    data = {
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error updating status: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for hook calls"""
    if len(sys.argv) < 2:
        print("Usage: update_status.py <status> [message]")
        print("Status options: working, waiting, idle, error")
        sys.exit(1)

    status = sys.argv[1].lower()
    message = sys.argv[2] if len(sys.argv) > 2 else ""

    # Validate status
    valid_statuses = ["working", "waiting", "idle", "error"]
    if status not in valid_statuses:
        print(f"Invalid status: {status}")
        print(f"Valid options: {', '.join(valid_statuses)}")
        sys.exit(1)

    if update_status(status, message):
        # Silent success for hooks
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
