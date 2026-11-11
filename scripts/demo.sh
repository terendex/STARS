#!/usr/bin/env bash
# Sets up, starts, stops or syncs the STARS demo CTF. The Linux version of demo.ps1.
#
#   bash scripts/demo.sh setup   # first time only: creates the admin, a demo team and the challenges
#   bash scripts/demo.sh start
#   bash scripts/demo.sh stop    # keeps accounts and scores
#   bash scripts/demo.sh sync    # after editing a demo challenge.yml
#
# The demo is a separate small CTF in demo/: 2 Easy challenges per category,
# none of them in the real event. It runs beside the real CTF on port 8100 and
# uses the same IP address. See "Demo CTF" in README.md.
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
DEMO="$ROOT/demo"
COMPOSE=(docker compose -f "$DEMO/docker-compose.yml")

bind_ip() { sed -n 's/^CTF_BIND_IP=//p' "$1" | tr -d '[:space:]'; }
new_secret() { head -c 32 /dev/urandom | base64 | tr -d '+/=\n'; }

start_demo() {
    if [[ ! -f $DEMO/.ctf/config ]]; then
        echo "The demo has not been set up yet. Run: bash scripts/demo.sh setup" >&2
        exit 1
    fi
    local ip
    ip=$(bind_ip "$ROOT/.env")
    # set-host.sh moves the demo's files whenever the real CTF changes IP.
    # This catches the case where they've drifted apart anyway.
    if [[ $(bind_ip "$DEMO/.env") != "$ip" ]]; then
        bash "$ROOT/scripts/set-host.sh" "$ip" --files-only >/dev/null
    fi
    "${COMPOSE[@]}" up -d --build --wait --wait-timeout 300
    "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
    echo "Demo CTF is on http://$ip:8100"
}

case ${1:-} in
    setup)
        if [[ ! -f $DEMO/.env ]]; then
            {
                echo "# Made by scripts/demo.sh setup. set-host.sh keeps CTF_BIND_IP on the same"
                echo "# address as the real CTF's .env."
                echo "CTF_BIND_IP=$(bind_ip "$ROOT/.env")"
                echo "SECRET_KEY=$(new_secret)"
                echo "DB_PASSWORD=$(new_secret)"
                echo "DB_ROOT_PASSWORD=$(new_secret)"
            } > "$DEMO/.env"
        fi
        # The first visitor to /setup becomes admin, so CTFd stays reachable from
        # this PC only until setup-ctfd.py has claimed it. The challenges start
        # afterwards, on the real address.
        CTF_BIND_IP=127.0.0.1 "${COMPOSE[@]}" up -d --wait --wait-timeout 300 ctfd
        "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/setup-ctfd.py demo
        "${COMPOSE[@]}" run --rm ctfcli challenge install
        start_demo
        ;;
    start) start_demo ;;
    stop) "${COMPOSE[@]}" stop ;;
    sync) "${COMPOSE[@]}" run --rm ctfcli challenge sync ;;
    *)
        echo "Usage: bash scripts/demo.sh setup|start|stop|sync" >&2
        exit 2
        ;;
esac
