#!/usr/bin/env bash
# Sets up STARS on a new Linux PC with one command. The Linux version of setup.ps1.
#
#   bash scripts/setup.sh
#
# It makes .env with new random passwords, builds and starts everything,
# finishes CTFd's setup with the event's rules, installs all 30 challenges,
# opens the CTF on this PC's network address, sets up the demo CTF, and turns on
# auto-host so the CTF follows your network. The admin password goes into
# LOGINS.txt. Running it again is safe: anything already set up is skipped.
#
#   --ip 192.168.1.20   use this address instead of detecting it
#   --no-demo           skip the demo CTF
#   --no-auto-host      don't install the auto-host cron jobs
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
IP=""
DEMO=1
AUTO_HOST=1
while [[ $# -gt 0 ]]; do
    case $1 in
        --ip) IP=${2:-}; shift 2 ;;
        --no-demo) DEMO=0; shift ;;
        --no-auto-host) AUTO_HOST=0; shift ;;
        *) echo "Usage: bash scripts/setup.sh [--ip <address>] [--no-demo] [--no-auto-host]" >&2; exit 2 ;;
    esac
done

new_secret() { head -c 32 /dev/urandom | base64 | tr -d '+/=\n'; }

# The address of the network card that reaches the internet, so not a Docker
# bridge. On a VPN, pass --ip with your Wi-Fi or LAN address instead.
lan_ip() { ip -4 route get 1.1.1.1 2>/dev/null | sed -nE 's/.* src ([0-9.]+).*/\1/p' | head -n 1; }

if ! docker info >/dev/null 2>&1; then
    echo "Can't reach Docker. Start it with: sudo systemctl start docker" >&2
    echo "If it's running, let your account use it: sudo usermod -aG docker \"\$USER\", then log out and back in." >&2
    exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
    echo "The Docker Compose plugin is missing. Install the docker-compose-plugin package." >&2
    exit 1
fi

[[ -n $IP ]] || IP=$(lan_ip)
if ! [[ $IP =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]]; then
    echo "No network found. Connect to the network the players will use, or pass --ip <address>." >&2
    exit 1
fi

cd "$ROOT"
if [[ ! -f .env ]]; then
    echo "Making .env with new random passwords."
    {
        echo "# Made by scripts/setup.sh. set-host.sh keeps CTF_BIND_IP on this PC's address."
        echo "CTF_BIND_IP=127.0.0.1"
        echo "SECRET_KEY=$(new_secret)"
        echo "DB_PASSWORD=$(new_secret)"
        echo "DB_ROOT_PASSWORD=$(new_secret)"
    } > .env
fi

if [[ ! -f .ctf/config ]]; then
    # The first visitor to /setup becomes admin, so CTFd stays reachable from
    # this PC only until setup-ctfd.py has claimed it.
    echo "Starting CTFd on this PC only (the first run downloads and builds everything, so it takes a few minutes)."
    CTF_BIND_IP=127.0.0.1 docker compose up -d --build --wait --wait-timeout 300 ctfd
    docker compose run --rm --entrypoint python ctfcli scripts/setup-ctfd.py main
    echo "Installing the challenges."
    docker compose run --rm ctfcli challenge install
else
    echo "CTFd is already set up (.ctf/config exists), so skipping that part."
fi

echo "Opening the CTF on $IP."
bash "$ROOT/scripts/set-host.sh" "$IP"

if [[ $DEMO == 1 ]]; then
    echo "Setting up the demo CTF."
    if [[ -f demo/.ctf/config ]]; then bash "$ROOT/scripts/demo.sh" start; else bash "$ROOT/scripts/demo.sh" setup; fi
fi

if [[ $AUTO_HOST == 1 ]]; then
    bash "$ROOT/scripts/install-auto-host.sh"
fi

echo
echo "Done. The CTF is on http://$IP:8000"
[[ $DEMO == 1 ]] && echo "The demo is on http://$IP:8100 (bash scripts/demo.sh stop to turn it off)."
echo "Admin passwords are in LOGINS.txt and demo/LOGINS.txt."
echo "If players can't connect, open the ports in your firewall (README.md, \"Linux\")."
echo "Next: register the players (README.md, \"Registering players\"), then test from a phone on the same network."
