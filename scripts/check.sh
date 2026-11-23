#!/usr/bin/env bash
# Checks every challenge.yml for common mistakes. It changes nothing. The Linux
# version of check.ps1. Run it before you sync:
#
#   bash scripts/check.sh          # every CTF
#   bash scripts/check.sh sits     # one CTF, by its folder name
#
# It runs scripts/check-challenges.py in the ctfcli container, so nothing needs
# installing, and CTFd doesn't need to be running.
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
# ctfcli doesn't use the address, but docker compose wants one before setup has
# made 2nd-star/.env.
CTF_BIND_IP=127.0.0.1 exec docker compose --progress quiet -f "$ROOT/2nd-star/docker-compose.yml" \
    run --rm --no-deps --entrypoint python ctfcli ../scripts/check-challenges.py "$@"
