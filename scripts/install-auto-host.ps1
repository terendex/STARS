<#
.SYNOPSIS
Sets up the two tasks that keep the CTF on your current network, or removes
them with -Remove.

.DESCRIPTION
- "STARS CTF - start at sign-in" starts Docker Desktop and the CTF when you sign in.
- "STARS CTF - follow network" moves the CTF to your new IP when Windows connects
  to a network, and checks every 5 minutes in case it missed one.

Both run as you, hidden, and need no admin rights. See scripts\auto-host.ps1.

    scripts\install-auto-host.ps1
    scripts\install-auto-host.ps1 -Remove
#>
param([switch]$Remove)

$ErrorActionPreference = 'Stop'
$signIn = 'STARS CTF - start at sign-in'
$follow = 'STARS CTF - follow network'

foreach ($name in $signIn, $follow) {
    if (Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $name -Confirm:$false
    }
}
if ($Remove) {
    Write-Host 'Removed. The CTF no longer starts or moves by itself.'
    return
}

$script = Join-Path $PSScriptRoot 'auto-host.ps1'
$user = "$env:USERDOMAIN\$env:USERNAME"
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 20)

# conhost --headless keeps a console window from flashing up each time.
function New-HiddenAction([string]$extra) {
    New-ScheduledTaskAction -Execute 'conhost.exe' `
        -Argument "--headless powershell.exe -NoProfile -NonInteractive -File `"$script`" $extra".TrimEnd()
}

Register-ScheduledTask -TaskName $signIn -Principal $principal -Settings $settings `
    -Action (New-HiddenAction '-AtSignIn') -Trigger (New-ScheduledTaskTrigger -AtLogOn -User $user) `
    -Description 'Starts Docker Desktop and the STARS CTF on the current network.' | Out-Null

# Event 10000 is Windows saying it has connected to a network. The delay lets
# the new IP settle first.
$class = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler
$onNetwork = New-CimInstance -CimClass $class -ClientOnly
$onNetwork.Enabled = $true
$onNetwork.Delay = 'PT15S'
$onNetwork.Subscription = '<QueryList><Query Id="0" Path="Microsoft-Windows-NetworkProfile/Operational">' +
    '<Select Path="Microsoft-Windows-NetworkProfile/Operational">*[System[(EventID=10000)]]</Select></Query></QueryList>'
$everyFiveMinutes = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)

Register-ScheduledTask -TaskName $follow -Principal $principal -Settings $settings `
    -Action (New-HiddenAction '') -Trigger @($onNetwork, $everyFiveMinutes) `
    -Description 'Moves the STARS CTF to this PC''s new IP when the network changes.' | Out-Null

Write-Host "Installed. The CTF now starts when you sign in and follows your network."
Write-Host "Activity is logged to logs\auto-host.log."
