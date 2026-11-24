#!/usr/bin/env bash
# Keeps the CTF on this PC's current network address. The Linux version of
# auto-host.ps1. The cron jobs from install-auto-host.sh run it.
#
#   --at-boot   start the CTF on the current network (run at boot)
#   (nothing)   if the IP has changed, move the CTF to it (run every 5 minutes)
#
# A CTF you've stopped stays stopped, and only its files are updated, so it
# starts on the right address next time. It also rebinds any running side CTF
# (the demos, Classic, SITS) left answering on an old address. It follows any
# network this PC joins. Everything it does goes in logs/auto-host.log.
set -uo pipefail
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
# The real CTF, 2nd Star. docker compose runs from its folder.
MAIN="$ROOT/2nd-star"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/auto-host.log"
# Set when the files were moved to a new IP while the CTF was stopped, so CTFd
# still shows the old address until it's running again.
PENDING="$LOG_DIR/addresses-pending"
mkdir -p "$LOG_DIR"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S')  $*" >> "$LOG"; }
lan_ip() { ip -4 route get 1.1.1.1 2>/dev/null | sed -nE 's/.* src ([0-9.]+).*/\1/p' | head -n 1; }
docker_ok() { docker info >/dev/null 2>&1; }
ctf_running() { [[ -n $(cd "$MAIN" && docker compose ps --status running -q ctfd 2>/dev/null) ]]; }

set_host() {
    bash "$ROOT/scripts/set-host.sh" "$@" 2>&1 |
        grep -E 'Updated the address|now use|CTF is now|failed|No \.ctf' |
        while IFS= read -r line; do log "  $line"; done
    return "${PIPESTATUS[0]}"
}

# Rebind any running side CTF (the demos, Classic, SITS) left answering on an old
# address, so its ports come back on $1. A stopped side is left alone; only a
# side whose files already point at $1 is touched, so this never fights set-host
# and can't loop: the recreate always lands on $1.
repair_sides() {
    local ip=$1 dir co side_bound cid h hostips stale out
    for dir in "$ROOT"/*/; do
        dir=${dir%/}
        [[ $dir == "$MAIN" ]] && continue
        [[ -f $dir/docker-compose.yml ]] || continue
        co=(compose -f "$dir/docker-compose.yml")
        [[ -n $(docker "${co[@]}" ps --status running -q ctfd 2>/dev/null) ]] || continue
        side_bound=$(sed -n 's/^CTF_BIND_IP=//p' "$dir/.env" 2>/dev/null | tr -d '[:space:]')
        [[ $side_bound == "$ip" ]] || continue
        stale=0
        for cid in $(docker "${co[@]}" ps -q 2>/dev/null); do
            hostips=$(docker inspect -f '{{range $p, $b := .HostConfig.PortBindings}}{{range $b}}{{.HostIp}} {{end}}{{end}}' "$cid" 2>/dev/null)
            for h in $hostips; do
                [[ -n $h && $h != 0.0.0.0 && $h != "$ip" ]] && stale=1
            done
        done
        (( stale )) || continue
        log "$(basename "$dir") is running but bound to an old address. Rebinding to $ip."
        if docker "${co[@]}" up -d --wait --wait-timeout 180 >/dev/null 2>&1; then
            if [[ -f $dir/.ctf/config ]]; then
                out=$(docker "${co[@]}" run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py . 2>/dev/null)
                [[ -n $out ]] && log "  $out"
            fi
            log "  $(basename "$dir") is now on $ip."
        else
            log "  docker compose up failed."
        fi
    done
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
bound=$(sed -n 's/^CTF_BIND_IP=//p' "$MAIN/.env" | tr -d '[:space:]')

if [[ $ip != "$bound" ]]; then
    if ctf_running; then
        log "Network changed: moving the CTF from $bound to $ip."
        set_host "$ip" && rm -f "$PENDING"
    else
        log "Network changed from $bound to $ip while the CTF is stopped. Updated its files only."
        set_host "$ip" --files-only && echo "$ip" > "$PENDING"
    fi
else
    # 2nd Star's files are already on $ip. Pull CTFd and any side CTF back into
    # line if something is still on an old address.
    if ctf_running && [[ -f $PENDING ]]; then
        log "The CTF is running again: updating the addresses in CTFd to $ip."
        output=$(cd "$MAIN" && docker compose run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py . 2>/dev/null)
        status=$?
        [[ -n $output ]] && log "  $output"
        [[ $status == 0 ]] && rm -f "$PENDING"
    fi
    repair_sides "$ip"
fi
