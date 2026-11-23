<#
.SYNOPSIS
Sets up, starts, stops or syncs the SITS Capture The Flag Competition 2026.

.DESCRIPTION
SITS is a separate competition CTF in the sits folder, made by Axel Jonas C.
Tangalin: casual-themed challenges with FLAG{...} flags. It has the same
mission clock, music, first blood, help queue and dynamic scoring as 2nd Star,
but its own CTFd, accounts and scores. It runs beside STARS on port 8300 and
uses the same IP address. See
sits\README.md.

    scripts\sits.ps1 setup      # first time only: the admin and the challenges
    scripts\sits.ps1 teams 15   # makes 15 teams of 3 accounts (logins in sits\LOGINS.txt)
    scripts\sits.ps1 start
    scripts\sits.ps1 stop       # keeps accounts and scores
    scripts\sits.ps1 sync       # after editing a challenge.yml in sits\challenges

Setup makes the admin the same as the real CTF's (the "Admin" entry in
2nd-star\LOGINS.txt), so one login works on every CTF.
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
$sits = Join-Path $root 'sits'
$envFile = Join-Path $sits '.env'
$ctfConfig = Join-Path $sits '.ctf\config'
$utf8 = New-Object System.Text.UTF8Encoding $false
$compose = @('compose', '-f', (Join-Path $sits 'docker-compose.yml'))

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

# The real CTF's admin, from the "Admin" entry in 2nd-star\LOGINS.txt: "  name / password".
function Get-MainAdmin {
    $logins = Join-Path $root '2nd-star\LOGINS.txt'
    if (-not (Test-Path $logins)) { return $null }
    $lines = Get-Content $logins
    $at = [Array]::IndexOf($lines, 'Admin')
    if ($at -lt 0 -or $at + 1 -ge $lines.Count) { return $null }
    if ($lines[$at + 1] -match '^\s+(\S+) / (\S+)') { return @{ Name = $Matches[1]; Password = $Matches[2] } }
    return $null
}

function Start-Sits {
    if (-not (Test-Path $ctfConfig)) { throw 'SITS has not been set up yet. Run: scripts\sits.ps1 setup' }

    # set-host.ps1 moves SITS's files whenever the real CTF changes IP. This
    # catches the case where they've drifted apart anyway.
    $ip = Get-BindIp (Join-Path $root '2nd-star\.env')
    if ((Get-BindIp $envFile) -ne $ip) {
        & (Join-Path $PSScriptRoot 'set-host.ps1') -Ip $ip -FilesOnly | Out-Null
    }

    Invoke-Compose up -d --build --wait --wait-timeout 300
    Invoke-Compose run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
    Write-Host "SITS is on http://${ip}:8300"
}

Push-Location $root
try {
    switch ($Action) {
        'setup' {
            if (-not (Test-Path $envFile)) {
                $ip = Get-BindIp (Join-Path $root '2nd-star\.env')
                $lines = @(
                    '# Made by scripts\sits.ps1 setup. set-host.ps1 keeps CTF_BIND_IP on the same',
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

            $admin = Get-MainAdmin
            if ($admin) {
                $env:STARS_ADMIN_NAME = $admin.Name
                $env:STARS_ADMIN_PASSWORD = $admin.Password
            }
            try {
                Invoke-Compose run --rm -e STARS_ADMIN_NAME -e STARS_ADMIN_PASSWORD --entrypoint python ctfcli ../scripts/setup-ctfd.py sits
            }
            finally {
                Remove-Item Env:STARS_ADMIN_NAME, Env:STARS_ADMIN_PASSWORD -ErrorAction SilentlyContinue
            }
            Invoke-Compose run --rm ctfcli challenge install
            Start-Sits
            Write-Host 'When you know the teams: scripts\sits.ps1 teams 15'
        }
        'teams' {
            if ($Count -lt 1) { throw 'Say how many teams, for example: scripts\sits.ps1 teams 15' }
            Invoke-Compose run --rm --entrypoint python ctfcli ../scripts/make-teams.py $Count
        }
        'start' { Start-Sits }
        'stop' { Invoke-Compose stop }
        'sync' { Invoke-Compose run --rm ctfcli challenge sync }
    }
}
finally {
    Pop-Location
}
