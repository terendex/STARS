#!/usr/bin/env bash
# Points the CTF at a new IP address. The Linux version of set-host.ps1.
#
#   bash scripts/set-host.sh 192.168.1.20
#   bash scripts/set-host.sh 192.168.1.20 --files-only
#
# Updates CTF_BIND_IP in .env and the address in every challenge's
# connection_info, republishes the ports on that address, and pushes the new
# addresses to CTFd. --files-only rewrites the files without starting anything.
#
# If the demo CTF in demo/ has been set up, its files move to the same IP too,
# and if it's running, it's republished there. A stopped demo stays stopped.
set -euo pipefail

IP=${1:-}
MODE=${2:-}
if ! [[ $IP =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]] || [[ -n $MODE && $MODE != --files-only ]]; then
    echo "Usage: bash scripts/set-host.sh <ip> [--files-only]" >&2
    exit 2
fi
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DEMO="$ROOT/demo"

for env_file in "$ROOT/.env" "$DEMO/.env"; do
    if [[ -f $env_file ]]; then
        sed -i -E "s/^CTF_BIND_IP=.*/CTF_BIND_IP=$IP/" "$env_file"
    fi
done

while IFS= read -r -d '' yml; do
    current=$(sed -nE 's/^connection_info:[^0-9]*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*/\1/p' "$yml" | head -n 1)
    if [[ -n $current && $current != "$IP" ]]; then
        sed -i -E "s/^(connection_info:[^0-9]*)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/\1$IP/" "$yml"
        echo "Updated ${yml#"$ROOT"/}"
    fi
done < <(find "$ROOT/challenges" "$DEMO/challenges" -name challenge.yml -print0 2>/dev/null)

# Keep the answer sheets' commands on the same address.
for answers in "$ROOT/ANSWERS.md" "$DEMO/ANSWERS.md"; do
    [[ -f $answers ]] || continue
    old=$(sed -nE 's/.*The commands use `([0-9.]+)`.*/\1/p' "$answers" | head -n 1)
    if [[ -n $old && $old != "$IP" ]]; then
        old_pattern=${old//./\\.}
        # Twice, because one pass can't match two addresses that share a separator.
        for _ in 1 2; do
            sed -i -E "s/(^|[^0-9.])$old_pattern([^0-9]|$)/\1$IP\2/g" "$answers"
        done
        echo "Updated ${answers#"$ROOT"/}"
    fi
done

# Republishes the demo CTF on the new address, but only if it's running.
move_demo() {
    [[ -f $DEMO/.ctf/config ]] || return 0
    local demo_compose=(docker compose -f "$DEMO/docker-compose.yml")
    [[ -n $("${demo_compose[@]}" ps --status running -q ctfd 2>/dev/null) ]] || return 0

    "${demo_compose[@]}" up -d --wait --wait-timeout 180 ||
        { echo "docker compose up failed for the demo CTF." >&2; exit 1; }
    "${demo_compose[@]}" run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py . ||
        { echo "Updating the addresses in the demo CTFd failed." >&2; exit 1; }
    echo "Demo CTF is now on http://$IP:8100"
}

if [[ $MODE == --files-only ]]; then
    echo "Files now use $IP. The CTF wasn't started."
    # The real CTF is stopped, but a running demo still has to move.
    move_demo
    exit 0
fi

cd "$ROOT"
# Rebinding restarts CTFd, so wait until it's healthy before updating it.
docker compose up -d --wait --wait-timeout 180 ||
    { echo "docker compose up failed. Is $IP assigned to this PC?" >&2; exit 1; }
if [[ -f $ROOT/.ctf/config ]]; then
    # Only the addresses: a full ctfcli sync would recreate every challenge's
    # flags, hints and files, which isn't safe while teams are playing.
    docker compose run --rm --entrypoint python ctfcli scripts/update-connection-info.py ||
        { echo "Updating the addresses in CTFd failed." >&2; exit 1; }
else
    echo "No .ctf/config yet, so CTFd was not updated."
fi
echo "CTF is now on http://$IP:8000"
move_demo
