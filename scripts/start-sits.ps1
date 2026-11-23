<#
.SYNOPSIS
Starts the SITS Capture The Flag Competition 2026 on this PC's current network.
The "Start SITS CTF" button on the desktop runs this.

.DESCRIPTION
Starts Docker Desktop first if it isn't running, moves the CTFs' files to this
PC's current IP (without starting 2nd Star), then starts SITS. Stop it with the
Stop STARS button, which stops every CTF on this PC.

    scripts\start-sits.ps1
#>
param([switch]$NoPause)

$ErrorActionPreference = 'Stop'

# The IPv4 address of the real network card in use, the same way auto-host.ps1
# finds it, so never Radmin, Tailscale or a virtual adapter.
function Get-LanIp {
    $physical = @(Get-NetAdapter -Physical | Where-Object Status -eq 'Up' | ForEach-Object ifIndex)
    $route = Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue |
        Where-Object { $physical -contains $_.ifIndex } |
        Sort-Object { $_.RouteMetric + (Get-NetIPInterface -InterfaceIndex $_.ifIndex -AddressFamily IPv4).InterfaceMetric } |
        Select-Object -First 1
    if (-not $route) { return $null }
    Get-NetIPAddress -InterfaceIndex $route.ifIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object { $_.IPAddress -notlike '169.254.*' -and $_.AddressState -eq 'Preferred' } |
        Select-Object -First 1 -ExpandProperty IPAddress
}

function Test-Docker {
    # docker writes to stderr while Docker Desktop is closed, which must not
    # count as this script failing.
    $ErrorActionPreference = 'Continue'
    docker info --format '{{.ServerVersion}}' 2>$null | Out-Null
    return $LASTEXITCODE -eq 0
}

try {
    Write-Host 'Starting the SITS competition. This takes a minute or two.'
    $ip = Get-LanIp
    if (-not $ip) { throw 'This PC is not connected to a network. Connect to the Wi-Fi the players will use, then try again.' }

    if (-not (Test-Docker)) {
        Write-Host 'Starting Docker Desktop...'
        if (-not (Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue)) {
            Start-Process (Join-Path $env:ProgramFiles 'Docker\Docker\Docker Desktop.exe')
        }
        $deadline = (Get-Date).AddMinutes(5)
        while (-not (Test-Docker)) {
            if ((Get-Date) -gt $deadline) { throw 'Docker Desktop did not start within 5 minutes. Open it, wait until it says it is running, then try again.' }
            Start-Sleep -Seconds 5
        }
    }

    # Moves the files only, so 2nd Star stays off if it is off.
    & (Join-Path $PSScriptRoot 'set-host.ps1') -Ip $ip -FilesOnly | Out-Null
    & (Join-Path $PSScriptRoot 'sits.ps1') start

    Write-Host ''
    Write-Host 'SITS is running.'
    Write-Host "  Players:       http://${ip}:8300"
    Write-Host '  Mission Clock: http://localhost:8003/admin/stars-timer (on this PC)'
    Write-Host '  Projector:     http://localhost:8003/timer (on this PC)'
    Write-Host 'The clock is as you left it. Press Start on the Mission Clock when everyone is ready.'
}
catch {
    Write-Host ''
    Write-Host "SITS did not start: $($_.Exception.Message)" -ForegroundColor Red
    if (-not $NoPause) { Read-Host 'Press Enter to close' | Out-Null }
    exit 1
}
if (-not $NoPause) { Read-Host 'Press Enter to close' | Out-Null }
