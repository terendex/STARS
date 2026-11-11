#!/usr/bin/env bash
# Keeps the CTF on this PC's current network address. The Linux version of
# auto-host.ps1. The cron jobs from install-auto-host.sh run it.
#
#   --at-boot   start the CTF on the current network (run at boot)
#   (nothing)   if the IP has changed, move the CTF to it (run every 5 minutes)
#
# A CTF you've stopped stays stopped, and only its files are updated, so it
# starts on the right address next time. It follows any network this PC joins.
# Everything it does goes in logs/auto-host.log.
set -uo pipefail
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/auto-host.log"
# Set when the files were moved to a new IP while the CTF was stopped, so CTFd
# still shows the old address until it's running again.
PENDING="$LOG_DIR/addresses-pending"
mkdir -p "$LOG_DIR"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S')  $*" >> "$LOG"; }
lan_ip() { ip -4 route get 1.1.1.1 2>/dev/null | sed -nE 's/.* src ([0-9.]+).*/\1/p' | head -n 1; }
docker_ok() { docker info >/dev/null 2>&1; }
ctf_running() { [[ -n $(cd "$ROOT" && docker compose ps --status running -q ctfd 2>/dev/null) ]]; }

set_host() {
    bash "$ROOT/scripts/set-host.sh" "$@" 2>&1 |
        grep -E 'Updated the address|now use|CTF is now|failed|No \.ctf' |
        while IFS= read -r line; do log "  $line"; done
    return "${PIPESTATUS[0]}"
}

# Only one copy at a time: boot and the 5-minute job can overlap.
exec 9>"$LOG_DIR/.auto-host.lock"
flock -n 9 || exit 0

# Keep the log from growing forever.
if [[ -f $LOG ]] && (( $(wc -c < "$LOG") > 200000 )); then
    tail -n 500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

if [[ ${1:-} == --at-boot ]]; then
    log "Booted."
    for _ in $(seq 60); do ip=$(lan_ip); [[ -n $ip ]] && break; sleep 10; done
    [[ -n ${ip:-} ]] || { log "  No network after 10 minutes, so the CTF was not started."; exit 1; }
    for _ in $(seq 60); do docker_ok && break; sleep 5; done
    docker_ok || { log "  Docker did not start within 5 minutes."; exit 1; }
    log "  Starting the CTF on $ip."
    set_host "$ip" && rm -f "$PENDING"
    exit 0
fi

# If Docker isn't running, leave everything alone.
docker_ok || exit 0
ip=$(lan_ip)
[[ -n $ip ]] || exit 0
bound=$(sed -n 's/^CTF_BIND_IP=//p' "$ROOT/.env" | tr -d '[:space:]')

if [[ $ip != "$bound" ]]; then
    if ctf_running; then
        log "Network changed: moving the CTF from $bound to $ip."
        set_host "$ip" && rm -f "$PENDING"
    else
        log "Network changed from $bound to $ip while the CTF is stopped. Updated its files only."
        set_host "$ip" --files-only && echo "$ip" > "$PENDING"
    fi
elif ctf_running && [[ -f $PENDING ]]; then
    log "The CTF is running again: updating the addresses in CTFd to $ip."
    output=$(cd "$ROOT" && docker compose run --rm --entrypoint python ctfcli scripts/update-connection-info.py 2>/dev/null)
    status=$?
    [[ -n $output ]] && log "  $output"
    [[ $status == 0 ]] && rm -f "$PENDING"
fi
