#!/usr/bin/env bash
# Sets up the cron jobs that keep the CTF on your current network, or removes
# them with --remove. The Linux version of install-auto-host.ps1.
#
#   bash scripts/install-auto-host.sh
#   bash scripts/install-auto-host.sh --start-at-boot
#   bash scripts/install-auto-host.sh --remove
#
# - Every 5 minutes, it moves the CTF to your new IP if the network changed. A
#   CTF that isn't running stays off; only its files are updated.
# - With --start-at-boot, it also starts the CTF at boot. Without it, STARS
#   doesn't start when the PC does.
# Both run as you, so your account must be able to use Docker without sudo.
# See scripts/auto-host.sh.
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="$ROOT/scripts/auto-host.sh"
MARK="# STARS auto-host"

if ! command -v crontab >/dev/null 2>&1; then
    echo "crontab isn't installed, so auto-host can't be set up. Install cron (the cron or cronie package)," >&2
    echo "or run 'bash scripts/set-host.sh <new IP>' yourself whenever your IP changes." >&2
    exit 1
fi
if [[ $SCRIPT == *"'"* ]]; then
    echo "The STARS folder's path contains a ' character, which cron can't handle. Move the folder and try again." >&2
    exit 1
fi

# Everything already in your crontab except our own lines.
others=$(crontab -l 2>/dev/null | grep -vF "$MARK" | grep -v '^$' || true)

if [[ ${1:-} == --remove ]]; then
    if [[ -n $others ]]; then printf '%s\n' "$others" | crontab -; else crontab -r 2>/dev/null || true; fi
    echo "Removed. The CTF no longer starts or moves by itself."
    exit 0
fi

at_boot=0
[[ ${1:-} == --start-at-boot ]] && at_boot=1
{
    [[ -n $others ]] && printf '%s\n' "$others"
    if (( at_boot )); then echo "@reboot bash '$SCRIPT' --at-boot $MARK"; fi
    echo "*/5 * * * * bash '$SCRIPT' $MARK"
} | crontab -

if (( at_boot )); then
    echo "Installed. The CTF now starts at boot and follows your network within 5 minutes."
else
    echo "Installed. The CTF follows your network within 5 minutes while it's running."
    echo "It doesn't start by itself: run docker compose up -d."
fi
echo "Activity is logged to logs/auto-host.log."
