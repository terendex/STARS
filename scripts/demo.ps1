<#
.SYNOPSIS
Sets up, starts, stops or syncs the STARS demo CTF.

.DESCRIPTION
The demo is a separate small CTF in the demo folder: 2 Easy challenges per
category, none of them in the real event. It has its own CTFd, accounts and
scores, runs beside the real CTF on port 8100, and uses the same IP address.
See "Demo CTF" in README.md.

    scripts\demo.ps1 setup   # first time only: creates the admin, a demo team and the challenges
    scripts\demo.ps1 start
    scripts\demo.ps1 stop    # keeps accounts and scores
    scripts\demo.ps1 sync    # after editing a demo challenge.yml
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('setup', 'start', 'stop', 'sync')]
    [string]$Action
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$demo = Join-Path $root 'demo'
$envFile = Join-Path $demo '.env'
$ctfConfig = Join-Path $demo '.ctf\config'
$utf8 = New-Object System.Text.UTF8Encoding $false
$compose = @('compose', '-f', (Join-Path $demo 'docker-compose.yml'))

function Get-BindIp($file) {
    (Select-String -Path $file -Pattern '^CTF_BIND_IP=(.*)$').Matches[0].Groups[1].Value.Trim()
}

function Invoke-Compose {
    # Docker writes progress to stderr, so only the exit code counts as failure.
    $ErrorActionPreference = 'Continue'
    & docker @compose @args
    if ($LASTEXITCODE -ne 0) { throw "docker compose $($args -join ' ') failed." }
}

function New-Secret {
    $bytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    return [Convert]::ToBase64String($bytes) -replace '[+/=]', ''
}

function Start-Demo {
    if (-not (Test-Path $ctfConfig)) { throw 'The demo has not been set up yet. Run: scripts\demo.ps1 setup' }

    # set-host.ps1 moves the demo's files whenever the real CTF changes IP.
    # This catches the case where they've drifted apart anyway.
    $ip = Get-BindIp (Join-Path $root '.env')
    if ((Get-BindIp $envFile) -ne $ip) {
        & (Join-Path $PSScriptRoot 'set-host.ps1') -Ip $ip -FilesOnly | Out-Null
    }

    Invoke-Compose up -d --build --wait --wait-timeout 300
    Invoke-Compose run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
    Write-Host "Demo CTF is on http://${ip}:8100"
}

Push-Location $root
try {
    switch ($Action) {
        'setup' {
            if (-not (Test-Path $envFile)) {
                $ip = Get-BindIp (Join-Path $root '.env')
                $lines = @(
                    '# Made by scripts\demo.ps1 setup. set-host.ps1 keeps CTF_BIND_IP on the same',
                    "# address as the real CTF's .env.",
                    "CTF_BIND_IP=$ip",
                    "SECRET_KEY=$(New-Secret)",
                    "DB_PASSWORD=$(New-Secret)",
                    "DB_ROOT_PASSWORD=$(New-Secret)"
                )
                [IO.File]::WriteAllText($envFile, ($lines -join "`n") + "`n", $utf8)
            }

            # The first visitor to /setup becomes admin, so CTFd stays reachable
            # from this PC only until setup-ctfd.py has claimed it. The challenges
            # start afterwards, on the real address.
            $env:CTF_BIND_IP = '127.0.0.1'
            try { Invoke-Compose up -d --wait --wait-timeout 300 ctfd }
            finally { Remove-Item Env:CTF_BIND_IP }

            Invoke-Compose run --rm --entrypoint python ctfcli ../scripts/setup-ctfd.py demo
            Invoke-Compose run --rm ctfcli challenge install
            Start-Demo
        }
        'start' { Start-Demo }
        'stop' { Invoke-Compose stop }
        'sync' { Invoke-Compose run --rm ctfcli challenge sync }
    }
}
finally {
    Pop-Location
}
