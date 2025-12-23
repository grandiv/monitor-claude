# PowerShell script to setup Claude Monitor to run at Windows startup
# Run this as Administrator

$taskName = "Claude Code Monitor"
$pythonPath = (Get-Command pythonw.exe).Source
$scriptPath = Join-Path $PSScriptRoot "claude_monitor.py"
$workingDir = $PSScriptRoot

Write-Host "Setting up Claude Code Monitor to run at startup..." -ForegroundColor Cyan
Write-Host "Task Name: $taskName" -ForegroundColor Gray
Write-Host "Python: $pythonPath" -ForegroundColor Gray
Write-Host "Script: $scriptPath" -ForegroundColor Gray
Write-Host ""

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task already exists. Removing old task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument "`"$scriptPath`"" `
    -WorkingDirectory $workingDir

# Create the trigger (at logon)
$trigger = New-ScheduledTaskTrigger -AtLogOn

# Create the principal (run as current user)
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0)

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Settings $settings `
        -Description "Monitors Claude Code status and displays in system tray" `
        -ErrorAction Stop

    Write-Host ""
    Write-Host "SUCCESS! Claude Code Monitor will now start automatically when you log in." -ForegroundColor Green
    Write-Host ""
    Write-Host "To start it now without restarting, run:" -ForegroundColor Cyan
    Write-Host "  pythonw.exe claude_monitor.py" -ForegroundColor White
    Write-Host ""
    Write-Host "To remove from startup, run:" -ForegroundColor Cyan
    Write-Host "  Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
}
catch {
    Write-Host ""
    Write-Host "ERROR: Failed to create scheduled task." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure you're running PowerShell as Administrator." -ForegroundColor Yellow
    exit 1
}
