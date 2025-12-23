# Quick Start - Hook-Based Monitor

Get your hook-based Claude Code monitor running in 3 steps!

## Step 1: Install Dependencies

```bash
cd C:\Projects\monitor-claude
pip install -r requirements.txt
```

## Step 2: Test the Monitor (Without Hooks First)

Start the monitor:
```bash
python claude_monitor_hooks.py
```

You should see a **gray circle icon** in your system tray (bottom-right).

In a **second command prompt**, test it manually:
```bash
cd C:\Projects\monitor-claude
python test_monitor.py
```

Follow the prompts. The icon should change colors:
- Gray → Green → Orange → Gray

## Step 3: Configure Claude Code Hooks

### Find Your Settings File

Claude Code settings are usually at:
```
C:\Users\HP\.claude\settings.json
```

### Add Hook Configuration

Open the settings file and add this hooks section (or merge if hooks already exist):

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

**Important Notes:**
- Use double backslashes: `C:\\Projects\\`
- If Python is not in your PATH, use full path: `C:\\Python311\\python.exe`
- Save the file
- Reload VS Code window (Ctrl+Shift+P → "Reload Window")

## Step 4: Use It!

1. **Keep the monitor running** (gray icon in tray)
2. **Open Claude Code** in VS Code
3. **Send a prompt** to Claude
4. **Watch the icon change**:
   - 🟢 Green = Claude is working
   - 🟡 Orange = Claude needs your input (you'll get a notification)
   - ⚪ Gray = Claude is idle

## Troubleshooting

**Icon doesn't change?**
- Check that `claude_status.json` exists in `C:\Projects\monitor-claude`
- Right-click icon → "Check Now"

**Hooks not working?**
- Verify Python path in hooks configuration
- Test manually: `python C:\Projects\monitor-claude\update_status.py working`
- Check Claude Code settings file for syntax errors

**No notifications?**
- Check Windows Settings → Notifications
- Enable notifications for "Claude Monitor"

## Auto-Start at Windows Boot

Press `Win + R`, type: `shell:startup`

Create a shortcut to: `C:\Projects\monitor-claude\run_monitor_hooks.bat`

---

For detailed setup and troubleshooting, see [SETUP.md](SETUP.md)
