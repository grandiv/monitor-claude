"""
Claude Code System Tray Monitor (Hook-Based Version)
Monitors Claude Code activity via hooks and displays status in Windows system tray
"""

import json
import time
import threading
from pathlib import Path
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification


class ClaudeStatus:
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"


class ClaudeMonitor(FileSystemEventHandler):
    def __init__(self):
        self.status = ClaudeStatus.IDLE
        self.status_file = Path(__file__).parent / "claude_status.json"
        self.icon = None
        self.last_notification_time = 0

        # Create initial status file if it doesn't exist
        if not self.status_file.exists():
            self.create_initial_status()

    def create_initial_status(self):
        """Create initial status file"""
        initial_status = {
            "status": ClaudeStatus.IDLE,
            "message": "Monitor started",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(initial_status, f, indent=2)
        except Exception as e:
            print(f"Error creating initial status: {e}")

    def create_icon_image(self, color):
        """Create a simple colored circle icon"""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw circle
        margin = 8
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=color,
            outline=(255, 255, 255, 180),
            width=2
        )

        return image

    def get_icon_for_status(self):
        """Get icon image based on current status"""
        colors = {
            ClaudeStatus.IDLE: (128, 128, 128, 255),      # Gray
            ClaudeStatus.WORKING: (0, 200, 0, 255),        # Green
            ClaudeStatus.WAITING: (255, 165, 0, 255),      # Orange
            ClaudeStatus.ERROR: (255, 0, 0, 255),          # Red
        }
        return self.create_icon_image(colors.get(self.status, (128, 128, 128, 255)))

    def update_icon(self):
        """Update the system tray icon"""
        if self.icon:
            self.icon.icon = self.get_icon_for_status()
            self.icon.title = f"Claude Code - {self.get_status_text()}"

    def get_status_text(self):
        """Get human-readable status text"""
        status_texts = {
            ClaudeStatus.IDLE: "Idle",
            ClaudeStatus.WORKING: "Working",
            ClaudeStatus.WAITING: "Needs Input!",
            ClaudeStatus.ERROR: "Error",
        }
        return status_texts.get(self.status, "Unknown")

    def read_status_file(self):
        """Read the current status from the status file"""
        if not self.status_file.exists():
            return None

        try:
            with open(self.status_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError:
            # File might be being written to
            time.sleep(0.05)
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            except:
                return None
        except Exception as e:
            print(f"Error reading status file: {e}")
            return None

    def check_status(self):
        """Check the status file and update accordingly"""
        status_data = self.read_status_file()

        if not status_data:
            return

        new_status = status_data.get('status', ClaudeStatus.IDLE)
        message = status_data.get('message', '')

        # Map status names from hooks
        if new_status == "working":
            new_status = ClaudeStatus.WORKING
        elif new_status == "waiting":
            new_status = ClaudeStatus.WAITING
        elif new_status == "idle":
            new_status = ClaudeStatus.IDLE
        elif new_status == "error":
            new_status = ClaudeStatus.ERROR

        # Update status if changed
        if new_status != self.status:
            old_status = self.status
            self.status = new_status
            self.update_icon()

            # Send notification for important state changes
            if new_status == ClaudeStatus.WAITING:
                # Avoid spamming notifications
                current_time = time.time()
                if current_time - self.last_notification_time > 10:  # 10 seconds cooldown
                    self.send_notification(
                        "Claude Needs Input",
                        message or "Claude Code is waiting for your response"
                    )
                    self.last_notification_time = current_time
            elif new_status == ClaudeStatus.IDLE and old_status == ClaudeStatus.WORKING:
                # Optionally notify when work is complete
                current_time = time.time()
                if current_time - self.last_notification_time > 10:
                    self.send_notification(
                        "Claude Code",
                        "Task completed"
                    )
                    self.last_notification_time = current_time

    def set_status(self, new_status):
        """Update status and icon"""
        if new_status != self.status:
            self.status = new_status
            self.update_icon()

    def send_notification(self, title, message):
        """Send Windows notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Claude Monitor",
                timeout=10
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def on_modified(self, event):
        """Called when status file is modified"""
        if event.src_path == str(self.status_file):
            time.sleep(0.05)  # Small delay to ensure file is written
            self.check_status()

    def monitor_loop(self):
        """Periodic check of status file"""
        while True:
            self.check_status()
            time.sleep(1)  # Check every second

    def quit_app(self, icon, item):
        """Quit the application"""
        icon.stop()

    def open_status_file(self, icon, item):
        """Open status file location"""
        import os
        os.startfile(self.status_file.parent)

    def force_check(self, icon, item):
        """Force a status check"""
        self.check_status()
        self.send_notification("Status Check", f"Current status: {self.get_status_text()}")

    def set_manual_status(self, icon, item, status):
        """Manually set status for testing"""
        self.set_status(status)
        self.send_notification("Manual Status", f"Set to: {self.get_status_text()}")

    def setup_tray_icon(self):
        """Setup the system tray icon"""
        menu = pystray.Menu(
            item('Status: ' + self.get_status_text(), lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            item('Check Now', self.force_check),
            item('Open Monitor Folder', self.open_status_file),
            pystray.Menu.SEPARATOR,
            item('Quit', self.quit_app)
        )

        self.icon = pystray.Icon(
            "claude_monitor",
            self.get_icon_for_status(),
            "Claude Code Monitor",
            menu
        )

    def run(self):
        """Start monitoring"""
        print("Claude Code Monitor Starting (Hook-Based)...")
        print(f"Watching status file: {self.status_file}")

        # Setup system tray icon
        self.setup_tray_icon()

        # Start file watcher
        observer = Observer()
        observer.schedule(self, str(self.status_file.parent), recursive=False)
        observer.start()
        print("File watcher started")

        # Start periodic monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()

        # Initial check
        self.check_status()

        print("Monitor running in system tray")
        print("\nTo test manually, run:")
        print(f"  python update_status.py working")
        print(f"  python update_status.py waiting")
        print(f"  python update_status.py idle")

        # Run the icon (this blocks)
        self.icon.run()


if __name__ == "__main__":
    monitor = ClaudeMonitor()
    monitor.run()
