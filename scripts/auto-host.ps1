<#
.SYNOPSIS
Keeps the CTF on this PC's current network address. The tasks from
install-auto-host.ps1 run it.

.DESCRIPTION
With -AtSignIn, it starts Docker Desktop and the CTF on the current network.

Without it, it runs whenever Windows connects to a network, and every 5 minutes.
If the IP has changed, it moves the CTF to the new one. A CTF you've stopped
stays stopped, and only its files are updated, so it starts on the right
address next time.

It follows any network this PC joins. Everything it does goes in logs\auto-host.log.
#>
param([switch]$AtSignIn)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$logDir = Join-Path $root 'logs'
$log = Join-Path $logDir 'auto-host.log'
# Set when the files were moved to a new IP while the CTF was stopped, so CTFd
# still shows the old address until it's running again.
$pending = Join-Path $logDir 'addresses-pending'
New-Item -ItemType Directory -Force $logDir | Out-Null

function Write-Log($message) {
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $message" | Add-Content -Path $log -Encoding utf8
}

# The IPv4 address of the real network card in use, so never Radmin, Tailscale
# or a virtual adapter.
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
    docker info --format '{{.ServerVersion}}' 2>$null | Out-Null
    return $LASTEXITCODE -eq 0
}

function Test-CtfRunning {
    return [bool](docker compose ps --status running -q ctfd 2>$null)
}

function Test-Port($ip, $port) {
    $client = New-Object Net.Sockets.TcpClient
    try { return $client.ConnectAsync($ip, $port).Wait(3000) -and $client.Connected }
    catch { return $false }
    finally { $client.Dispose() }
}

function Invoke-SetHost([hashtable]$arguments) {
    try {
        & (Join-Path $PSScriptRoot 'set-host.ps1') @arguments *>&1 |
            Where-Object { "$_" -match 'Updated the address|now use|CTF is now|failed|No \.ctf' } |
            ForEach-Object { Write-Log "  $_" }
        return $true
    }
    catch {
        Write-Log "  FAILED: $($_.Exception.Message)"
        return $false
    }
}

# A sign-in and a network change often happen together, so only one copy runs.
$mutex = New-Object Threading.Mutex($false, 'Local\STARS-auto-host')
try { $owned = $mutex.WaitOne(0) } catch [Threading.AbandonedMutexException] { $owned = $true }
if (-not $owned) { exit 0 }

Push-Location $root
try {
    if ((Test-Path $log) -and (Get-Item $log).Length -gt 200KB) {
        $keep = Get-Content $log -Tail 500
        Set-Content -Path $log -Value $keep -Encoding utf8
    }

    if ($AtSignIn) {
        Write-Log 'Signed in.'
        $deadline = (Get-Date).AddMinutes(10)
        while (-not ($ip = Get-LanIp) -and (Get-Date) -lt $deadline) { Start-Sleep -Seconds 10 }
        if (-not $ip) { Write-Log '  No network after 10 minutes, so the CTF was not started.'; exit 1 }

        if (-not (Test-Docker)) {
            if (-not (Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue)) {
                Write-Log '  Starting Docker Desktop.'
                Start-Process (Join-Path $env:ProgramFiles 'Docker\Docker\Docker Desktop.exe')
            }
            $deadline = (Get-Date).AddMinutes(5)
            while (-not (Test-Docker) -and (Get-Date) -lt $deadline) { Start-Sleep -Seconds 5 }
            if (-not (Test-Docker)) { Write-Log '  Docker Desktop did not start within 5 minutes.'; exit 1 }
        }

        Write-Log "  Starting the CTF on $ip."
        if (Invoke-SetHost @{ Ip = $ip }) { Remove-Item $pending -ErrorAction SilentlyContinue }
        exit 0
    }

    # If Docker Desktop isn't running, you've closed it, so leave everything alone.
    if (-not (Test-Docker)) { exit 0 }
    $ip = Get-LanIp
    if (-not $ip) { exit 0 }

    $bound = (Select-String -Path (Join-Path $root '.env') -Pattern '^CTF_BIND_IP=(.*)$').Matches[0].Groups[1].Value.Trim()
    $running = Test-CtfRunning

    if ($ip -ne $bound) {
        if ($running) {
            Write-Log "Network changed: moving the CTF from $bound to $ip."
            if (Invoke-SetHost @{ Ip = $ip }) { Remove-Item $pending -ErrorAction SilentlyContinue }
        }
        else {
            Write-Log "Network changed from $bound to $ip while the CTF is stopped. Updated its files only."
            if (Invoke-SetHost @{ Ip = $ip; FilesOnly = $true }) { Set-Content -Path $pending -Value $ip }
        }
    }
    elseif ($running -and (Test-Path $pending)) {
        Write-Log "The CTF is running again: updating the addresses in CTFd to $ip."
        docker compose run --rm --entrypoint python ctfcli scripts/update-connection-info.py 2>$null |
            ForEach-Object { Write-Log "  $_" }
        if ($LASTEXITCODE -eq 0) { Remove-Item $pending -ErrorAction SilentlyContinue }
    }
    elseif ($running) {
        # Same IP, but if the network dropped and came back, Docker may have
        # stopped listening on it. Only act if CTFd itself is healthy.
        $healthy = (docker inspect -f '{{.State.Health.Status}}' (docker compose ps -q ctfd) 2>$null) -eq 'healthy'
        if ($healthy -and -not ((Test-Port $ip 8000) -and (Test-Port $ip 2220))) {
            Write-Log "CTFd is healthy but $ip isn't answering. Republishing the ports."
            docker compose up -d --force-recreate --wait --wait-timeout 180 ctfd edge *>&1 | Out-Null
            Write-Log "  docker compose exit code: $LASTEXITCODE"
        }
    }
}
finally {
    Pop-Location
    $mutex.ReleaseMutex()
}
