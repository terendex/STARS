#!/usr/bin/env bash
# Sets up, starts, stops or syncs the SITS Capture The Flag Competition 2026.
# The Linux version of sits.ps1.
#
#   bash scripts/sits.sh setup      # first time only: the admin and the challenges
#   bash scripts/sits.sh teams 15   # makes 15 teams of 3 accounts (logins in sits/LOGINS.txt)
#   bash scripts/sits.sh start
#   bash scripts/sits.sh stop       # keeps accounts and scores
#   bash scripts/sits.sh sync       # after editing a challenge.yml in sits/challenges
#
# SITS is a separate competition CTF in sits/, made by Axel Jonas C. Tangalin,
# with the same mission clock, music, first blood, help queue and dynamic
# scoring as 2nd Star. It runs beside STARS on port 8300 and uses the same IP
# address. Setup makes its admin the same as the real CTF's (the "Admin" entry
# in 2nd-star/LOGINS.txt). See sits/README.md.
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SITS="$ROOT/sits"
COMPOSE=(docker compose -f "$SITS/docker-compose.yml")

bind_ip() { sed -n 's/^CTF_BIND_IP=//p' "$1" | tr -d '[:space:]'; }
new_secret() { head -c 32 /dev/urandom | base64 | tr -d '+/=\n'; }
# The real CTF's admin: the line after "Admin" in LOGINS.txt, "  name / password".
main_admin() { [[ -f $ROOT/2nd-star/LOGINS.txt ]] && awk 'found { print; exit } $0 == "Admin" { found = 1 }' "$ROOT/2nd-star/LOGINS.txt" || true; }

start_sits() {
    if [[ ! -f $SITS/.ctf/config ]]; then
        echo "SITS has not been set up yet. Run: bash scripts/sits.sh setup" >&2
        exit 1
    fi
    local ip
    ip=$(bind_ip "$ROOT/2nd-star/.env")
    if [[ $(bind_ip "$SITS/.env") != "$ip" ]]; then
        bash "$ROOT/scripts/set-host.sh" "$ip" --files-only >/dev/null
    fi
    "${COMPOSE[@]}" up -d --build --wait --wait-timeout 300
    "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py .
    echo "SITS is on http://$ip:8300"
}

case ${1:-} in
    setup)
        if [[ ! -f $SITS/.env ]]; then
            {
                echo "# Made by scripts/sits.sh setup. set-host.sh keeps CTF_BIND_IP on the same"
                echo "# address as the real CTF's .env."
                echo "CTF_BIND_IP=$(bind_ip "$ROOT/2nd-star/.env")"
                echo "SECRET_KEY=$(new_secret)"
                echo "DB_PASSWORD=$(new_secret)"
                echo "DB_ROOT_PASSWORD=$(new_secret)"
            } > "$SITS/.env"
        fi
        CTF_BIND_IP=127.0.0.1 "${COMPOSE[@]}" up -d --wait --wait-timeout 300 ctfd
        admin=$(main_admin)
        name=$(sed -E 's#^ +([^ ]+) / .*#\1#' <<<"$admin")
        password=$(sed -E 's#^ +[^ ]+ / ([^ ]+).*#\1#' <<<"$admin")
        STARS_ADMIN_NAME=${admin:+$name} STARS_ADMIN_PASSWORD=${admin:+$password} \
            "${COMPOSE[@]}" run --rm -e STARS_ADMIN_NAME -e STARS_ADMIN_PASSWORD --entrypoint python ctfcli ../scripts/setup-ctfd.py sits
        "${COMPOSE[@]}" run --rm ctfcli challenge install
        start_sits
        echo "When you know the teams: bash scripts/sits.sh teams 15"
        ;;
    teams)
        if ! [[ ${2:-} =~ ^[1-9][0-9]*$ ]]; then
            echo "Say how many teams, for example: bash scripts/sits.sh teams 15" >&2
            exit 2
        fi
        "${COMPOSE[@]}" run --rm --entrypoint python ctfcli ../scripts/make-teams.py "$2"
        ;;
    start) start_sits ;;
    stop) "${COMPOSE[@]}" stop ;;
    sync) "${COMPOSE[@]}" run --rm ctfcli challenge sync ;;
    *)
        echo "Usage: bash scripts/sits.sh setup|teams <count>|start|stop|sync" >&2
        exit 2
        ;;
esac
