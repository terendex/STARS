<#
.SYNOPSIS
Puts "Start STARS", "Stop STARS" and "Start SITS CTF" buttons on the desktop,
or removes them with -Remove.

.DESCRIPTION
Start STARS runs scripts\start-stars.ps1 (Docker Desktop, then the real CTF on
this PC's current network). Stop STARS runs scripts\stop-stars.ps1 (the real
CTF, STARS Classic, both demos and SITS). Start SITS CTF runs
scripts\start-sits.ps1. Each opens a small window that says what it did. Run this again if you move the STARS folder.

    scripts\install-shortcuts.ps1
    scripts\install-shortcuts.ps1 -Remove
#>
param([switch]$Remove)

$ErrorActionPreference = 'Stop'
$desktop = [Environment]::GetFolderPath('Desktop')
$buttons = @(
    @{ Name = 'Start STARS'; Script = 'start-stars.ps1'; Text = 'Starts Docker Desktop and the STARS CTF on this PC''s network.' },
    @{ Name = 'Stop STARS'; Script = 'stop-stars.ps1'; Text = 'Stops every CTF on this PC: STARS, STARS Classic, both demos and SITS. Scores are kept.' },
    @{ Name = 'Start SITS CTF'; Script = 'start-sits.ps1'; Text = 'Starts Docker Desktop and the SITS Capture The Flag Competition 2026.' }
)

foreach ($button in $buttons) {
    $path = Join-Path $desktop "$($button.Name).lnk"
    if ($Remove) {
        Remove-Item $path -ErrorAction SilentlyContinue
        continue
    }
    $shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($path)
    $shortcut.TargetPath = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
    $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$(Join-Path $PSScriptRoot $button.Script)`""
    $shortcut.WorkingDirectory = Split-Path -Parent $PSScriptRoot
    $shortcut.Description = $button.Text
    $icon = Join-Path (Split-Path -Parent $PSScriptRoot) 'branding\stars.ico'
    if (Test-Path $icon) { $shortcut.IconLocation = $icon }
    $shortcut.Save()
}

if ($Remove) { Write-Host 'Removed the Start STARS, Stop STARS and Start SITS CTF buttons from the desktop.' }
else { Write-Host "Added Start STARS, Stop STARS and Start SITS CTF to the desktop ($desktop)." }
