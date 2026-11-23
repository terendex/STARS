<#
.SYNOPSIS
Checks every challenge.yml for common mistakes. It changes nothing.

.DESCRIPTION
Run it before you sync, after adding or editing a challenge:

    scripts\check.ps1            # every CTF
    scripts\check.ps1 sits       # one CTF, by its folder name

It runs scripts\check-challenges.py in the ctfcli container, so nothing needs
installing, and CTFd doesn't need to be running. docs\making-challenges.md
explains each rule.
#>
$root = Split-Path -Parent $PSScriptRoot
# ctfcli doesn't use the address, but docker compose wants one before setup has
# made 2nd-star\.env.
# Put back afterwards, so a later docker compose up in this window isn't affected.
$saved = $env:CTF_BIND_IP
$env:CTF_BIND_IP = '127.0.0.1'
try {
    & docker compose --progress quiet -f (Join-Path $root '2nd-star\docker-compose.yml') run --rm --no-deps --entrypoint python ctfcli ../scripts/check-challenges.py @args
    $code = $LASTEXITCODE
}
finally {
    $env:CTF_BIND_IP = $saved
}
exit $code
