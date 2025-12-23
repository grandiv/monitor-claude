@echo off
REM Run Claude Code Monitor (Hook-Based Version)
REM Use pythonw.exe to run without console window

cd /d "%~dp0"
call venv\Scripts\activate.bat
pythonw.exe claude_monitor_hooks.py
