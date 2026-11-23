#!/bin/bash
# 11 UMi: the flag is on a beacon on the challenges' private network (the
# beacon service in docker-compose.yml), on one port between 4000 and 4999.
# Only this server can reach it, so players scan for it with nc -z, then
# connect. This account just needs a shell; nc is installed for everyone.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=umi11
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:beaconhunt" | chpasswd

home="/home/$user"
mkdir -p "$home"
cat > "$home/notes.txt" <<'TEXT'
The beacon is at the address "beacon" on the observatory's private network.
It answers on exactly one port between 4000 and 4999.
After it sends you something, press Ctrl+C to get back to the prompt.
Nothing is stored here: the flag is whatever the beacon sends you.
TEXT

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/notes.txt"
