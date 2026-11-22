<#
.SYNOPSIS
Points the CTF at a new IP address.

.DESCRIPTION
Updates CTF_BIND_IP in .env and the address in every challenge's connection_info,
republishes the ports on that address, and pushes the new addresses to CTFd.
Run it from anywhere, for example after your Wi-Fi IP changes:

    scripts\set-host.ps1 -Ip 192.168.68.101

With auto-host installed, this happens by itself.

The side CTFs move with it: the demo in demo\ and STARS Classic in classic\.
If one has been set up, its files move to the same IP too, and if it's
running, it's republished there. A stopped one stays stopped.
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d{1,3}(\.\d{1,3}){3}$')]
    [string]$Ip,

    # Only rewrite the files, without starting anything. auto-host.ps1 uses this
    # while the CTF is stopped.
    [switch]$FilesOnly
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding $false

# The CTFs that run beside the real one, on the same IP.
$sides = @(
    @{ Dir = (Join-Path $root 'demo'); Name = 'Demo CTF'; Port = 8100 },
    @{ Dir = (Join-Path $root 'classic'); Name = 'STARS Classic'; Port = 8200 }
)

foreach ($envFile in @((Join-Path $root '.env')) + @($sides | ForEach-Object { Join-Path $_.Dir '.env' })) {
    if (-not (Test-Path $envFile)) { continue }
    $text = [IO.File]::ReadAllText($envFile, $utf8)
    [IO.File]::WriteAllText($envFile, ($text -replace '(?m)^CTF_BIND_IP=.*$', "CTF_BIND_IP=$Ip"), $utf8)
}

$challenges = @((Join-Path $root 'challenges')) + @($sides | ForEach-Object { Join-Path $_.Dir 'challenges' }) |
    Where-Object { Test-Path $_ }
Get-ChildItem $challenges -Recurse -Filter challenge.yml | ForEach-Object {
    $text = [IO.File]::ReadAllText($_.FullName, $utf8)
    $updated = [regex]::Replace(
        $text,
        '(?m)^(connection_info:.*?)\b\d{1,3}(\.\d{1,3}){3}\b',
        { param($match) $match.Groups[1].Value + $Ip }
    )
    if ($updated -cne $text) {
        [IO.File]::WriteAllText($_.FullName, $updated, $utf8)
        Write-Host "Updated $($_.FullName.Substring($root.Length + 1))"
    }
}

# Keep the answer sheets' commands on the same address.
foreach ($answers in @((Join-Path $root 'ANSWERS.md')) + @($sides | ForEach-Object { Join-Path $_.Dir 'ANSWERS.md' })) {
    if (-not (Test-Path $answers)) { continue }
    $text = [IO.File]::ReadAllText($answers, $utf8)
    $old = [regex]::Match($text, 'The commands use `([\d.]+)`').Groups[1].Value
    if ($old -and $old -ne $Ip) {
        $pattern = '(?<![\d.])' + [regex]::Escape($old) + '(?!\d)'
        [IO.File]::WriteAllText($answers, [regex]::Replace($text, $pattern, $Ip), $utf8)
        Write-Host "Updated $($answers.Substring($root.Length + 1))"
    }
}

# Republishes the demo and STARS Classic on the new address, but only the ones
# that are running.
function Move-Sides {
    $ErrorActionPreference = 'Continue'
    foreach ($side in $sides) {
        if (-not (Test-Path (Join-Path $side.Dir '.ctf\config'))) { continue }
        $sideCompose = @('compose', '-f', (Join-Path $side.Dir 'docker-compose.yml'))
        if (-not (docker @sideCompose ps --status running -q ctfd 2>$null)) { continue }

        docker @sideCompose up -d --wait --wait-timeout 180
        if ($LASTEXITCODE -ne 0) { throw "docker compose up failed for $($side.Name)." }
        docker @sideCompose run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
        if ($LASTEXITCODE -ne 0) { throw "Updating the addresses in $($side.Name)'s CTFd failed." }
        Write-Host "$($side.Name) is now on http://${Ip}:$($side.Port)"
    }
}

if ($FilesOnly) {
    Write-Host "Files now use $Ip. The CTF wasn't started."
    # The real CTF is stopped, but a running demo or Classic still has to move.
    Move-Sides
    return
}

# Docker writes progress to stderr, which must not count as a failure here.
# The exit codes below are what decide that.
$ErrorActionPreference = 'Continue'

Push-Location $root
try {
    # Rebinding restarts CTFd, so wait until it's healthy before updating it.
    docker compose up -d --wait --wait-timeout 180
    if ($LASTEXITCODE -ne 0) { throw "docker compose up failed. Is $Ip assigned to this PC?" }

    if (Test-Path (Join-Path $root '.ctf\config')) {
        # Only the addresses: a full ctfcli sync would recreate every challenge's
        # flags, hints and files, which isn't safe while teams are playing.
        docker compose run --rm --entrypoint python ctfcli scripts/update-connection-info.py
        if ($LASTEXITCODE -ne 0) { throw 'Updating the addresses in CTFd failed.' }
    }
    else {
        Write-Host 'No .ctf/config yet, so CTFd was not updated.'
    }
}
finally {
    Pop-Location
}

Write-Host "CTF is now on http://${Ip}:8000"
Move-Sides
