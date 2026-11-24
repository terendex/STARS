#!/usr/bin/env bash
# Points the CTF at a new IP address. The Linux version of set-host.ps1.
#
#   bash scripts/set-host.sh 192.168.1.20
#   bash scripts/set-host.sh 192.168.1.20 --files-only
#
# Updates CTF_BIND_IP in 2nd-star/.env and the address in every challenge's
# connection_info, republishes the ports on that address, and pushes the new
# addresses to CTFd. --files-only rewrites the files without starting anything.
#
# The side CTFs move with it: the demos in demo/ and demo2/, STARS Classic in
# classic/ and the SITS competition in sits/.
# If one has been set up, its files move to the same IP too, and if it's
# running, it's republished there. A stopped one stays stopped.
set -euo pipefail

IP=${1:-}
MODE=${2:-}
if ! [[ $IP =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]] || [[ -n $MODE && $MODE != --files-only ]]; then
    echo "Usage: bash scripts/set-host.sh <ip> [--files-only]" >&2
    exit 2
fi
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
# The real CTF, 2nd Star. Its .env holds the IP every CTF uses.
MAIN="$ROOT/2nd-star"
# The CTFs that run beside the real one, on the same IP, as folder:port.
# A new event only needs adding here (and in set-host.ps1).
SIDES=("demo:8100" "demo2:8500" "classic:8200" "sits:8300")
# Every CTF's folder: 2nd Star first, then the sides.
FOLDERS=("$MAIN")
for side in "${SIDES[@]}"; do FOLDERS+=("$ROOT/${side%%:*}"); done

for folder in "${FOLDERS[@]}"; do
    env_file="$folder/.env"
    if [[ -f $env_file ]]; then
        sed -i -E "s/^CTF_BIND_IP=.*/CTF_BIND_IP=$IP/" "$env_file"
    fi
done

while IFS= read -r -d '' yml; do
    # The IP may follow a name with digits in it, like ssh umi11@<ip>.
    current=$(sed -nE 's/^connection_info:(.*[^0-9.])?([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*/\2/p' "$yml" | head -n 1)
    if [[ -n $current && $current != "$IP" ]]; then
        sed -i -E "s/^(connection_info:(.*[^0-9.])?)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/\1$IP/" "$yml"
        echo "Updated ${yml#"$ROOT"/}"
    fi
done < <(for folder in "${FOLDERS[@]}"; do [[ -d $folder/challenges ]] && find "$folder/challenges" -name challenge.yml -print0; done)

# Keep the answer sheets' commands on the same address.
for folder in "${FOLDERS[@]}"; do
    answers="$folder/ANSWERS.md"
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

# Republishes the demo and STARS Classic on the new address, but only the ones
# that are running.
move_sides() {
    local side dir port side_compose
    for side in "${SIDES[@]}"; do
        dir="$ROOT/${side%%:*}"
        port=${side##*:}
        [[ -f $dir/.ctf/config ]] || continue
        side_compose=(docker compose -f "$dir/docker-compose.yml")
        [[ -n $("${side_compose[@]}" ps --status running -q ctfd 2>/dev/null) ]] || continue

        "${side_compose[@]}" up -d --wait --wait-timeout 180 ||
            { echo "docker compose up failed for ${side%%:*}." >&2; exit 1; }
        "${side_compose[@]}" run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py . ||
            { echo "Updating the addresses in ${side%%:*}'s CTFd failed." >&2; exit 1; }
        echo "${side%%:*} is now on http://$IP:$port"
    done
}

if [[ $MODE == --files-only ]]; then
    echo "Files now use $IP. The CTF wasn't started."
    # The real CTF is stopped, but a running demo or Classic still has to move.
    move_sides
    exit 0
fi

cd "$MAIN"
# Rebinding restarts CTFd, so wait until it's healthy before updating it.
docker compose up -d --wait --wait-timeout 180 ||
    { echo "docker compose up failed. Is $IP assigned to this PC?" >&2; exit 1; }
if [[ -f $MAIN/.ctf/config ]]; then
    # Only the addresses: a full ctfcli sync would recreate every challenge's
    # flags, hints and files, which isn't safe while teams are playing.
    docker compose run --rm --entrypoint python ctfcli ../scripts/update-connection-info.py . ||
        { echo "Updating the addresses in CTFd failed." >&2; exit 1; }
else
    echo "No .ctf/config yet, so CTFd was not updated."
fi
echo "CTF is now on http://$IP:8000"
move_sides
