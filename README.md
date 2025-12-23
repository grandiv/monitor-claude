# Claude Code System Tray Monitor

> 🚀 A Windows system tray application that monitors [Claude Code](https://code.claude.com/) status in real-time and displays it next to your WiFi, volume, and battery icons.

Never miss when Claude needs your input again! This lightweight monitor runs in your system tray and shows you at a glance what Claude is doing.

## ✨ Features

- **🟢 Real-time Status** - Instantly see when Claude is working, waiting, or idle
- **📍 System Tray Icon** - Unobtrusive icon right next to your WiFi/battery
- **🔔 Smart Notifications** - Get alerted only when Claude needs your attention
- **⚡ Lightweight** - Minimal resource usage, runs silently in the background
- **🎨 Color-Coded** - Visual indicators at a glance:
  - 🟢 **Green** - Claude is actively working on your request
  - 🟡 **Orange** - Claude is waiting for your input (notification sent!)
  - ⚪ **Gray** - Claude is idle
  - 🔴 **Red** - Error detected

## 🎯 Use Case

Working on other tasks while Claude Code is running? This monitor lets you:
- Browse the web while Claude works
- Switch between applications without losing track
- Get notified instantly when Claude needs your confirmation
- Avoid constantly checking VS Code for status updates

## 📋 Requirements

- Windows 10 or 11
- Python 3.8 or higher
- [Claude Code](https://code.claude.com/) (VS Code extension or CLI)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd C:\Projects\monitor-claude
pip install -r requirements.txt
```

### 2. Test the Monitor

```bash
python claude_monitor_hooks.py
```

Look for a **gray circle icon** in your system tray (bottom-right corner).

In another terminal, test it:
```bash
python test_monitor.py
```

Watch the icon change colors! 🎨

### 3. Configure Claude Code Hooks

Open your Claude Code settings file (usually at `C:\Users\[YourUsername]\.claude\settings.json`) and add:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python C:\\Projects\\monitor-claude\\update_status.py working"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python C:\\Projects\\monitor-claude\\update_status.py waiting"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python C:\\Projects\\monitor-claude\\update_status.py idle"
          }
        ]
      }
    ]
  }
}
```

**Important:**
- Use double backslashes in Windows paths: `C:\\Projects\\`
- Adjust the path to match your installation directory
- If Python is not in your PATH, use the full path: `C:\\Python311\\python.exe`

### 4. Reload VS Code

Press `Ctrl + Shift + P` → Type "Reload Window" → Press Enter

### 5. Done! 🎉

Now use Claude Code normally. The system tray icon will show Claude's real-time status!

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step installation guide
- **[SETUP.md](SETUP.md)** - Detailed configuration and troubleshooting
- **[START_HERE.md](START_HERE.md)** - Project overview and file guide

## 🔧 How It Works

```
┌─────────────┐  events   ┌──────────────┐  writes   ┌─────────────┐
│ Claude Code │─────────▶ │    Hooks     │─────────▶ │ Status File │
│  (VS Code)  │           │  (settings)  │           │   (.json)   │
└─────────────┘           └──────────────┘           └─────────────┘
                                                             │
                                                             │ watches
                                                             ▼
                                                      ┌─────────────┐
                                                      │   Monitor   │
                                                      │ (tray icon) │
                                                      └─────────────┘
```

1. **Claude Code triggers hooks** when events occur (tool use, waiting for input, finished)
2. **Hooks call update script** (`update_status.py`) to write status to a JSON file
3. **Monitor watches the file** and updates the system tray icon
4. **You get visual feedback** and notifications when attention is needed

This approach uses Claude Code's official [hooks system](https://code.claude.com/docs/en/hooks.md) for reliable, real-time status tracking.

## 🎨 Customization

### Change Icon Colors

Edit `claude_monitor_hooks.py` around line 52:

```python
colors = {
    ClaudeStatus.IDLE: (128, 128, 128, 255),      # Gray
    ClaudeStatus.WORKING: (0, 200, 0, 255),        # Green
    ClaudeStatus.WAITING: (255, 165, 0, 255),      # Orange
    ClaudeStatus.ERROR: (255, 0, 0, 255),          # Red
}
```

### Adjust Check Frequency

Edit line 148 to change how often the monitor checks for updates:

```python
time.sleep(1)  # Check every second (change as needed)
```

### Disable Completion Notifications

Comment out lines 138-145 to stop notifications when Claude finishes a task.

## 🔄 Auto-Start at Windows Boot

### Easy Method

1. Press `Win + R`, type: `shell:startup`, press Enter
2. Create a shortcut to `C:\Projects\monitor-claude\run_monitor_hooks.bat`

### Task Scheduler Method

Run `setup_startup.bat` as Administrator for a more robust startup configuration.

## 🐛 Troubleshooting

### Icon stays gray even when Claude is working

**Cause:** Hooks not configured or not triggering

**Solution:**
1. Verify hooks are in `~/.claude/settings.json`
2. Test manually: `python update_status.py working`
3. Check if `claude_status.json` is created/updated
4. Ensure Python path in hooks is correct

### No notifications appear

**Cause:** Windows notifications disabled

**Solution:**
1. Open Settings → System → Notifications
2. Enable notifications for "Claude Monitor"

### Hooks not executing

**Cause:** Python not found in PATH

**Solution:**
```bash
where python
```

Use the full path in hooks:
```json
"command": "C:\\Python311\\python.exe C:\\Projects\\monitor-claude\\update_status.py working"
```

For more troubleshooting, see [SETUP.md](SETUP.md).

## 📁 Project Structure

```
monitor-claude/
├── claude_monitor_hooks.py   # Main monitor application
├── update_status.py           # Status updater (called by hooks)
├── claude_status.json         # Status file (auto-generated)
├── test_monitor.py            # Test script
├── requirements.txt           # Python dependencies
├── run_monitor_hooks.bat      # Easy launcher
├── setup_startup.bat/ps1      # Auto-startup setup
├── claude_hooks_config.json   # Example configuration
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── README.md                  # This file
├── QUICKSTART.md              # Quick setup guide
├── SETUP.md                   # Detailed documentation
└── START_HERE.md              # Project overview
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

MIT License - Free to use and modify

## 🔗 Resources

- [Claude Code Documentation](https://code.claude.com/docs)
- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks.md)

## 💡 Why This Approach?

Initially, this project attempted to monitor a `transcript.json` file, but **Claude Code doesn't use that file format**. This version uses Claude Code's official [hooks system](https://code.claude.com/docs/en/hooks.md), which provides:

✅ Real-time, accurate status updates
✅ Official API support (future-proof)
✅ Event-driven architecture (efficient)
✅ No polling or guessing required

## ⭐ Show Your Support

If you find this tool useful, please give it a star! It helps others discover the project.

---

**Made with ❤️ for the Claude Code community**
