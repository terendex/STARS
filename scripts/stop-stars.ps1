<#
.SYNOPSIS
Stops STARS: the real CTF, STARS Classic and the demo. Accounts, scores and the
clock are kept. The "Stop STARS" button on the desktop runs this.

    scripts\stop-stars.ps1
#>
param([switch]$NoPause)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot

docker info --format '{{.ServerVersion}}' 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Docker Desktop is not running, so STARS is already off.'
}
else {
    $ctfs = @(
        @{ Name = 'The real CTF (2nd Star)'; File = Join-Path $root 'docker-compose.yml' },
        @{ Name = 'STARS Classic'; File = Join-Path $root 'classic\docker-compose.yml' },
        @{ Name = 'The demo'; File = Join-Path $root 'demo\docker-compose.yml' }
    )
    foreach ($ctf in $ctfs) {
        if (-not (docker compose -f $ctf.File ps --status running -q 2>$null)) {
            Write-Host "$($ctf.Name) was already off."
            continue
        }
        Write-Host "Stopping $($ctf.Name)..."
        docker compose -f $ctf.File stop 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) { Write-Host "  stopped." } else { Write-Host "  did not stop cleanly. Try again." -ForegroundColor Red }
    }
    Write-Host ''
    Write-Host 'STARS is off. Accounts and scores are kept. Start it again with Start STARS.'
}
if (-not $NoPause) { Read-Host 'Press Enter to close' | Out-Null }
