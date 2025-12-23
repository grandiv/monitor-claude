# Hook-Based Monitor Setup Guide

This version uses Claude Code's hook system to track status in real-time.

## How It Works

1. **Claude Code hooks** trigger when events happen (working, waiting for input, finished)
2. **Hooks call** `update_status.py` to write status to a file
3. **Monitor watches** the status file and updates the tray icon
4. **You get notified** when Claude needs your attention

## Installation Steps

### Step 1: Install Dependencies

If you haven't already:

```bash
cd C:\Projects\monitor-claude
pip install -r requirements.txt
```

### Step 2: Configure Claude Code Hooks

You need to add hooks to your Claude Code settings file.

#### Option A: Using Claude Code UI (Easiest)

1. **Open Claude Code** in VS Code
2. **Find your settings file** by running one of these commands in Claude Code:
   - On Windows: Type in Claude Code: "Where is my settings file?"
   - Or check: `C:\Users\HP\.claude\settings.json`

3. **Add the hooks configuration** - Open your settings file and add or merge this:

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

**IMPORTANT:**
- If you already have hooks configured, merge these into your existing hooks section
- Make sure the path uses double backslashes: `C:\\Projects\\monitor-claude\\`
- If Python is not in your PATH, use full path: `C:\\Python311\\python.exe`

4. **Save the file** and restart Claude Code (reload VS Code window)

#### Option B: Manual Configuration

1. Navigate to your Claude Code config directory:
   - Windows: `C:\Users\HP\.claude\`
   - Or check `%USERPROFILE%\.claude\`

2. Open or create `settings.json`

3. Copy the hooks configuration from above

4. Save and restart Claude Code

### Step 3: Run the Monitor

```bash
cd C:\Projects\monitor-claude
python claude_monitor_hooks.py
```

You should see:
- Console message: "Claude Code Monitor Starting (Hook-Based)..."
- A gray circle icon in your system tray

### Step 4: Test It!

#### Test 1: Manual Test

In a separate command prompt:

```bash
cd C:\Projects\monitor-claude

# Test working status
python update_status.py working

# Wait a moment, then test waiting status
python update_status.py waiting

# Test idle status
python update_status.py idle
```

Watch the tray icon change colors!

#### Test 2: Real Claude Code Test

1. **Open Claude Code** in VS Code
2. **Send a prompt** to Claude (like "hello")
3. **Watch the icon**:
   - Should turn **green** when Claude starts working
   - Should turn **orange** when Claude asks a question
   - Should turn **gray** when Claude finishes

## Troubleshooting

### Hooks not triggering

**Check if Python path is correct:**
```bash
where python
```

Then update the hooks to use the full path:
```json
"command": "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python311\\python.exe C:\\Projects\\monitor-claude\\update_status.py working"
```

**Verify hooks are configured:**
1. Open your Claude Code settings file
2. Make sure the hooks section exists
3. Check for syntax errors (missing commas, brackets)

**Test hook manually:**
Open Command Prompt and run:
```bash
python C:\Projects\monitor-claude\update_status.py working
```

Should create/update `claude_status.json` in the monitor folder.

### Icon doesn't change color

**Check if status file is being created:**
```bash
dir C:\Projects\monitor-claude\claude_status.json
```

**Check if monitor is running:**
- Look for the gray icon in system tray
- Check Task Manager for `python.exe`

**Force a check:**
- Right-click the tray icon
- Click "Check Now"

### Monitor not starting

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**Check for errors:**
Run with verbose output:
```bash
python claude_monitor_hooks.py
```

Look for error messages in console.

### Notifications not appearing

**Windows notification settings:**
1. Press `Win + I` (Settings)
2. Go to System > Notifications
3. Make sure notifications are enabled
4. Look for "Claude Monitor" and enable it

## Running at Startup

To have the monitor start automatically:

### Option 1: Startup Folder

1. Press `Win + R` and type: `shell:startup`
2. Create a shortcut to: `C:\Projects\monitor-claude\run_monitor_hooks.bat`

### Option 2: Task Scheduler

Use the `setup_startup.ps1` script (need to update it for the hooks version).

## How Hooks Work

### ToolUse Hook
- **Triggers:** When Claude uses any tool (Read, Write, Bash, etc.)
- **Action:** Sets status to "working" (green icon)
- **Why:** Indicates Claude is actively doing something

### Notification Hook
- **Triggers:** When Claude sends a notification (usually when asking for permission or input)
- **Action:** Sets status to "waiting" (orange icon) and sends notification
- **Why:** You need to provide input or permission

### Stop Hook
- **Triggers:** When Claude finishes responding
- **Action:** Sets status to "idle" (gray icon)
- **Why:** Task is complete, Claude is waiting for your next prompt

## Advanced Configuration

### Customize Notifications

Edit `claude_monitor_hooks.py` around line 140 to change when notifications are sent:

```python
# Disable completion notifications
elif new_status == ClaudeStatus.IDLE and old_status == ClaudeStatus.WORKING:
    # Comment out this section to disable
    pass
```

### Change Check Interval

Edit `claude_monitor_hooks.py` line 148:

```python
time.sleep(1)  # Change to check more/less frequently
```

### Add More Hook Events

You can add hooks for other events like:
- `PromptSubmit` - When you submit a prompt
- `Error` - When an error occurs
- Custom matchers to trigger on specific tool uses

See Claude Code hooks documentation for more events.

## Status File Format

The `claude_status.json` file contains:

```json
{
  "status": "working",
  "message": "Claude is working",
  "timestamp": "2025-12-23 15:30:45"
}
```

You can manually edit this file to test the monitor.

## Uninstalling

1. Right-click tray icon and select "Quit"
2. Remove hooks from Claude Code `settings.json`
3. Remove from startup (if added)
4. Delete `C:\Projects\monitor-claude` folder

## Support

If you encounter issues:
1. Check the console output when running the monitor
2. Verify `claude_status.json` is being created/updated
3. Test hooks manually with `update_status.py`
4. Make sure Python is in your PATH or use full path in hooks

## What's Different from File-Based Version

**Old version:**
- ❌ Tried to watch `transcript.json` (doesn't exist in Claude Code)
- ❌ Couldn't detect real-time status
- ❌ Didn't work

**New version:**
- ✅ Uses Claude Code's official hook system
- ✅ Real-time status updates
- ✅ Works with actual Claude Code events
- ✅ More reliable and future-proof
