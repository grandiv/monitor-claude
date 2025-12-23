# 🚀 Start Here - Claude Code Monitor

Welcome! This is a system tray monitor that tracks Claude Code's status in real-time.

## What You Have

A complete Windows system tray application that:
- Shows Claude Code's status (working/waiting/idle) in your taskbar
- Sends notifications when Claude needs your input
- Uses Claude Code's official hooks system for real-time updates

## Quick Start

### 1. Install Dependencies

```bash
cd C:\Projects\monitor-claude
pip install -r requirements.txt
```

### 2. Test It

Start the monitor:
```bash
python claude_monitor_hooks.py
```

You'll see a gray circle in your system tray.

In another terminal, test it:
```bash
python test_monitor.py
```

Watch the icon change colors!

### 3. Configure Hooks

Add this to `C:\Users\HP\.claude\settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [{"type": "command", "command": "python C:\\Projects\\monitor-claude\\update_status.py working"}]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [{"type": "command", "command": "python C:\\Projects\\monitor-claude\\update_status.py waiting"}]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [{"type": "command", "command": "python C:\\Projects\\monitor-claude\\update_status.py idle"}]
      }
    ]
  }
}
```

Reload VS Code (Ctrl+Shift+P → Reload Window) and you're done!

## Documentation

- **[README.md](README.md)** - Main documentation (start here for GitHub)
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup guide
- **[SETUP.md](SETUP.md)** - Detailed configuration and troubleshooting

## Files Overview

**Main Application:**
- `claude_monitor_hooks.py` - The monitor (runs in system tray)
- `update_status.py` - Status updater (called by Claude Code hooks)
- `test_monitor.py` - Test script to verify everything works

**Configuration:**
- `requirements.txt` - Python dependencies
- `claude_hooks_config.json` - Example hooks configuration
- `.gitignore` - Git ignore rules

**Utilities:**
- `run_monitor_hooks.bat` - Easy launcher (auto-activates venv)
- `setup_startup.bat/ps1` - Scripts to auto-start at Windows boot

**Documentation:**
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick setup guide
- `SETUP.md` - Detailed guide
- `START_HERE.md` - This file
- `LICENSE` - MIT License

## Status Indicators

- 🟢 **Green** = Claude is working
- 🟡 **Orange** = Claude needs your input (you'll get a notification!)
- ⚪ **Gray** = Claude is idle
- 🔴 **Red** = Error

## Need Help?

1. **Quick setup:** See [QUICKSTART.md](QUICKSTART.md)
2. **Troubleshooting:** See [SETUP.md](SETUP.md)
3. **Full docs:** See [README.md](README.md)

## Ready for GitHub?

Yes! The codebase is clean and documented. Just:

1. Make sure `claude_status.json` is in `.gitignore` ✅ (done)
2. Make sure `venv/` is in `.gitignore` ✅ (done)
3. Push to GitHub!

```bash
git init
git add .
git commit -m "Initial commit: Claude Code system tray monitor"
git remote add origin https://github.com/yourusername/monitor-claude.git
git push -u origin main
```

---

**Enjoy!** 🎉
