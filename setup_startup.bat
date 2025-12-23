@echo off
REM Setup Claude Monitor to run at startup using Task Scheduler
REM Run this as Administrator

echo Setting up Claude Code Monitor to run at startup...
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0setup_startup.ps1"

pause
