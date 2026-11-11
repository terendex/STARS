<#
.SYNOPSIS
Sets up STARS on a new Windows PC with one command.

.DESCRIPTION
Run this once after downloading the project, with Docker Desktop running:

    powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

It makes .env with new random passwords, builds and starts everything, finishes
CTFd's setup with the event's rules, installs all 30 challenges, opens the CTF
on this PC's Wi-Fi address, sets up the demo CTF, and turns on auto-host so the
CTF follows your network. The admin password goes into LOGINS.txt.

Running it again is safe: anything already set up is skipped.

    -Ip 192.168.1.20   use this address instead of detecting it
    -NoDemo            skip the demo CTF
    -NoAutoHost        don't install the auto-host tasks
#>
param(
    [ValidatePattern('^\d{1,3}(\.\d{1,3}){3}$')]
    [string]$Ip,
    [switch]$NoDemo,
    [switch]$NoAutoHost
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding $false

function Invoke-Compose {
    # Docker writes progress to stderr, so only the exit code counts as failure.
    $ErrorActionPreference = 'Continue'
    & docker compose @args
    if ($LASTEXITCODE -ne 0) { throw "docker compose $($args -join ' ') failed." }
}

function New-Secret {
    $bytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    return [Convert]::ToBase64String($bytes) -replace '[+/=]', ''
}

# The IPv4 address of the real network card in use, the same way auto-host.ps1
# finds it, so never a VPN or virtual adapter.
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

Push-Location $root
try {
    $ErrorActionPreference = 'Continue'
    docker info --format '{{.ServerVersion}}' 2>$null | Out-Null
    $dockerOk = $LASTEXITCODE -eq 0
    $ErrorActionPreference = 'Stop'
    if (-not $dockerOk) { throw 'Docker is not running. Start Docker Desktop, wait for it to finish starting, then run this again.' }

    if (-not $Ip) { $Ip = Get-LanIp }
    if (-not $Ip) { throw 'No network found. Connect to the Wi-Fi the players will use, or pass -Ip <address>.' }

    $envFile = Join-Path $root '.env'
    if (-not (Test-Path $envFile)) {
        Write-Host 'Making .env with new random passwords.'
        $lines = @(
            '# Made by scripts\setup.ps1. set-host.ps1 keeps CTF_BIND_IP on this PC''s address.',
            'CTF_BIND_IP=127.0.0.1',
            "SECRET_KEY=$(New-Secret)",
            "DB_PASSWORD=$(New-Secret)",
            "DB_ROOT_PASSWORD=$(New-Secret)"
        )
        [IO.File]::WriteAllText($envFile, ($lines -join "`n") + "`n", $utf8)
    }

    if (-not (Test-Path (Join-Path $root '.ctf\config'))) {
        # The first visitor to /setup becomes admin, so CTFd stays reachable from
        # this PC only until setup-ctfd.py has claimed it.
        Write-Host 'Starting CTFd on this PC only (the first run downloads and builds everything, so it takes a few minutes).'
        $env:CTF_BIND_IP = '127.0.0.1'
        try { Invoke-Compose up -d --build --wait --wait-timeout 300 ctfd }
        finally { Remove-Item Env:CTF_BIND_IP }

        Invoke-Compose run --rm --entrypoint python ctfcli scripts/setup-ctfd.py main
        Write-Host 'Installing the challenges.'
        Invoke-Compose run --rm ctfcli challenge install
    }
    else {
        Write-Host 'CTFd is already set up (.ctf\config exists), so skipping that part.'
    }

    Write-Host "Opening the CTF on $Ip."
    & (Join-Path $PSScriptRoot 'set-host.ps1') -Ip $Ip

    if (-not $NoDemo) {
        Write-Host 'Setting up the demo CTF.'
        if (Test-Path (Join-Path $root 'demo\.ctf\config')) { & (Join-Path $PSScriptRoot 'demo.ps1') start }
        else { & (Join-Path $PSScriptRoot 'demo.ps1') setup }
    }

    if (-not $NoAutoHost) {
        & (Join-Path $PSScriptRoot 'install-auto-host.ps1')
    }

    Write-Host ''
    Write-Host "Done. The CTF is on http://${Ip}:8000"
    if (-not $NoDemo) { Write-Host "The demo is on http://${Ip}:8100 (scripts\demo.ps1 stop to turn it off)." }
    Write-Host 'Admin passwords are in LOGINS.txt and demo\LOGINS.txt.'
    Write-Host 'Next: register the players (README.md, "Registering players"), then test from a phone on the same Wi-Fi.'
}
finally {
    Pop-Location
}
