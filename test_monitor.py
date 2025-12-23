"""
Test script to simulate Claude Code hooks and verify monitor works
Run this to test the monitor without needing to configure Claude Code hooks first
"""

import subprocess
import time
import sys
from pathlib import Path

def run_update(status, message=""):
    """Run the update_status script"""
    script_path = Path(__file__).parent / "update_status.py"
    cmd = [sys.executable, str(script_path), status]
    if message:
        cmd.append(message)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Set status to: {status}")
            return True
        else:
            print(f"✗ Error setting status to {status}")
            print(f"  {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Failed to run update: {e}")
        return False


def main():
    print("=" * 60)
    print("Claude Code Monitor - Hook Simulation Test")
    print("=" * 60)
    print()
    print("This script simulates what Claude Code hooks will do.")
    print("Make sure the monitor is running before starting this test!")
    print()
    input("Press Enter to start the test (or Ctrl+C to cancel)...")
    print()

    # Test sequence simulating Claude Code workflow
    tests = [
        ("idle", "Monitor started", 2),
        ("working", "Claude started working on your request", 3),
        ("working", "Claude is reading files", 2),
        ("working", "Claude is using tools", 3),
        ("waiting", "Claude needs your input", 4),
        ("working", "Claude continuing after your input", 3),
        ("idle", "Claude finished the task", 3),
    ]

    print("Starting test sequence...\n")

    for i, (status, message, delay) in enumerate(tests, 1):
        print(f"Test {i}/{len(tests)}: {message}")
        if run_update(status, message):
            print(f"  Waiting {delay} seconds...")
            print(f"  → Check your system tray icon!")
            time.sleep(delay)
            print()
        else:
            print("  Test failed, stopping.")
            return 1

    print("=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print()
    print("Did you see the icon change colors?")
    print("  - Gray   = Idle")
    print("  - Green  = Working")
    print("  - Orange = Waiting for input")
    print()
    print("Did you receive notifications when status changed to 'waiting'?")
    print()
    print("If everything worked, you're ready to configure Claude Code hooks!")
    print("See SETUP.md for instructions.")
    print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(0)
