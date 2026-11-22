<#
.SYNOPSIS
Sets up, starts, stops or syncs STARS Classic.

.DESCRIPTION
STARS Classic is the original 36 challenges from the first orientation, kept as
their own CTF in the classic folder. It has the same mission clock, music and
dynamic scoring as the real CTF, but its own CTFd, accounts and scores. It runs
beside the real CTF on port 8200 and uses the same IP address. See
"STARS Classic" in README.md.

    scripts\classic.ps1 setup      # first time only: creates the admin and the challenges
    scripts\classic.ps1 teams 15   # makes 15 teams of 3 accounts (logins in classic\LOGINS.txt)
    scripts\classic.ps1 start
    scripts\classic.ps1 stop       # keeps accounts and scores
    scripts\classic.ps1 sync       # after editing a challenge.yml in classic\challenges
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('setup', 'start', 'stop', 'sync', 'teams')]
    [string]$Action,

    # How many teams "teams" makes.
    [int]$Count = 0
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$classic = Join-Path $root 'classic'
$envFile = Join-Path $classic '.env'
$ctfConfig = Join-Path $classic '.ctf\config'
$utf8 = New-Object System.Text.UTF8Encoding $false
$compose = @('compose', '-f', (Join-Path $classic 'docker-compose.yml'))

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

function Start-Classic {
    if (-not (Test-Path $ctfConfig)) { throw 'STARS Classic has not been set up yet. Run: scripts\classic.ps1 setup' }

    # set-host.ps1 moves Classic's files whenever the real CTF changes IP. This
    # catches the case where they've drifted apart anyway.
    $ip = Get-BindIp (Join-Path $root '.env')
    if ((Get-BindIp $envFile) -ne $ip) {
        & (Join-Path $PSScriptRoot 'set-host.ps1') -Ip $ip -FilesOnly | Out-Null
    }

    Invoke-Compose up -d --build --wait --wait-timeout 300
    Invoke-Compose run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
    Write-Host "STARS Classic is on http://${ip}:8200"
}

Push-Location $root
try {
    switch ($Action) {
        'setup' {
            if (-not (Test-Path $envFile)) {
                $ip = Get-BindIp (Join-Path $root '.env')
                $lines = @(
                    '# Made by scripts\classic.ps1 setup. set-host.ps1 keeps CTF_BIND_IP on the same',
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

            Invoke-Compose run --rm --entrypoint python ctfcli ../scripts/setup-ctfd.py classic
            Invoke-Compose run --rm ctfcli challenge install
            Start-Classic
            Write-Host 'Next, make the teams: scripts\classic.ps1 teams 15'
        }
        'teams' {
            if ($Count -lt 1) { throw 'Say how many teams, for example: scripts\classic.ps1 teams 15' }
            Invoke-Compose run --rm --entrypoint python ctfcli ../scripts/make-teams.py $Count
        }
        'start' { Start-Classic }
        'stop' { Invoke-Compose stop }
        'sync' { Invoke-Compose run --rm ctfcli challenge sync }
    }
}
finally {
    Pop-Location
}
