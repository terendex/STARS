#!/usr/bin/env bash
# Sets up, starts, stops or syncs STARS Classic. The Linux version of classic.ps1.
#
#   bash scripts/classic.sh setup      # first time only: creates the admin and the challenges
#   bash scripts/classic.sh teams 15   # makes 15 teams of 3 accounts (logins in classic/LOGINS.txt)
#   bash scripts/classic.sh start
#   bash scripts/classic.sh stop       # keeps accounts and scores
#   bash scripts/classic.sh sync       # after editing a challenge.yml in classic/challenges
#
# STARS Classic is the original 36 challenges from the first orientation, kept as
# their own CTF in classic/, with the same mission clock, music and dynamic
# scoring as the real CTF. It runs beside the real CTF on port 8200 and uses the
# same IP address. See classic/README.md.
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CLASSIC="$ROOT/classic"
COMPOSE=(docker compose -f "$CLASSIC/docker-compose.yml")

bind_ip() { sed -n 's/^CTF_BIND_IP=//p' "$1" | tr -d '[:space:]'; }
new_secret() { head -c 32 /dev/urandom | base64 | tr -d '+/=\n'; }

start_classic() {
    if [[ ! -f $CLASSIC/.ctf/config ]]; then
        echo "STARS Classic has not been set up yet. Run: bash scripts/classic.sh setup" >&2
        exit 1
    fi
    local ip
    ip=$(bind_ip "$ROOT/2nd-star/.env")
    # set-host.sh moves Classic's files whenever the real CTF changes IP. This
    # catches the case where they've drifted apart anyway.
    if [[ $(bind_ip "$CLASSIC/.env") != "$ip" ]]; then
        bash "$ROOT/scripts/set-host.sh" "$ip" --files-only >/dev/null
    fi
    "${COMPOSE[@]}" up -d --build --wait --wait-timeout 300
    "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
    echo "STARS Classic is on http://$ip:8200"
}

case ${1:-} in
    setup)
        if [[ ! -f $CLASSIC/.env ]]; then
            {
                echo "# Made by scripts/classic.sh setup. set-host.sh keeps CTF_BIND_IP on the same"
                echo "# address as the real CTF's .env."
                echo "CTF_BIND_IP=$(bind_ip "$ROOT/2nd-star/.env")"
                echo "SECRET_KEY=$(new_secret)"
                echo "DB_PASSWORD=$(new_secret)"
                echo "DB_ROOT_PASSWORD=$(new_secret)"
            } > "$CLASSIC/.env"
        fi
        # The first visitor to /setup becomes admin, so CTFd stays reachable from
        # this PC only until setup-ctfd.py has claimed it. The challenges start
        # afterwards, on the real address.
        CTF_BIND_IP=127.0.0.1 "${COMPOSE[@]}" up -d --wait --wait-timeout 300 ctfd
        "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/setup-ctfd.py classic
        "${COMPOSE[@]}" run --rm ctfcli challenge install
        start_classic
        echo "Next, make the teams: bash scripts/classic.sh teams 15"
        ;;
    teams)
        if ! [[ ${2:-} =~ ^[1-9][0-9]*$ ]]; then
            echo "Say how many teams, for example: bash scripts/classic.sh teams 15" >&2
            exit 2
        fi
        "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/make-teams.py "$2"
        ;;
    start) start_classic ;;
    stop) "${COMPOSE[@]}" stop ;;
    sync) "${COMPOSE[@]}" run --rm ctfcli challenge sync ;;
    *)
        echo "Usage: bash scripts/classic.sh setup|teams <count>|start|stop|sync" >&2
        exit 2
        ;;
esac
