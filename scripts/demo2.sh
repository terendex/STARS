#!/usr/bin/env bash
# Sets up, starts, stops or syncs the 2nd STARS demo CTF. The Linux version of demo2.ps1.
#
#   bash scripts/demo2.sh setup   # first time only: creates the admin, a demo team and the challenges
#   bash scripts/demo2.sh start
#   bash scripts/demo2.sh stop    # keeps accounts and scores
#   bash scripts/demo2.sh sync    # after editing a demo challenge.yml
#
# The 2nd demo is a separate small CTF in demo2/: one Medium challenge per
# category, none of them in a real event. It works like the first demo, runs
# beside the real CTF on port 8500 and uses the same IP address. See
# demo2/README.md.
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DEMO="$ROOT/demo2"
COMPOSE=(docker compose -f "$DEMO/docker-compose.yml")

bind_ip() { sed -n 's/^CTF_BIND_IP=//p' "$1" | tr -d '[:space:]'; }
new_secret() { head -c 32 /dev/urandom | base64 | tr -d '+/=\n'; }

start_demo() {
    if [[ ! -f $DEMO/.ctf/config ]]; then
        echo "The 2nd demo has not been set up yet. Run: bash scripts/demo2.sh setup" >&2
        exit 1
    fi
    local ip
    ip=$(bind_ip "$ROOT/2nd-star/.env")
    # set-host.sh moves the demo's files whenever the real CTF changes IP.
    # This catches the case where they've drifted apart anyway.
    if [[ $(bind_ip "$DEMO/.env") != "$ip" ]]; then
        bash "$ROOT/scripts/set-host.sh" "$ip" --files-only >/dev/null
    fi
    "${COMPOSE[@]}" up -d --build --wait --wait-timeout 300
    "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
    echo "The 2nd demo is on http://$ip:8500"
}

case ${1:-} in
    setup)
        if [[ ! -f $DEMO/.env ]]; then
            {
                echo "# Made by scripts/demo2.sh setup. set-host.sh keeps CTF_BIND_IP on the same"
                echo "# address as the real CTF's .env."
                echo "CTF_BIND_IP=$(bind_ip "$ROOT/2nd-star/.env")"
                echo "SECRET_KEY=$(new_secret)"
                echo "DB_PASSWORD=$(new_secret)"
                echo "DB_ROOT_PASSWORD=$(new_secret)"
            } > "$DEMO/.env"
        fi
        # The first visitor to /setup becomes admin, so CTFd stays reachable from
        # this PC only until setup-ctfd.py has claimed it. The challenges start
        # afterwards, on the real address.
        CTF_BIND_IP=127.0.0.1 "${COMPOSE[@]}" up -d --wait --wait-timeout 300 ctfd
        "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/setup-ctfd.py demo2
        "${COMPOSE[@]}" run --rm ctfcli challenge install
        start_demo
        ;;
    start) start_demo ;;
    stop) "${COMPOSE[@]}" stop ;;
    sync) "${COMPOSE[@]}" run --rm ctfcli challenge sync ;;
    *)
        echo "Usage: bash scripts/demo2.sh setup|start|stop|sync" >&2
        exit 2
        ;;
esac
