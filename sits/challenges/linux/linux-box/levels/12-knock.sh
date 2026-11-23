#!/bin/bash
# Knock Knock (Medium): the flag is on the "doorbell" server on the challenges'
# private network (the doorbell service in docker-compose.yml), on one port
# between 5000 and 5999. Only this box can reach it, so players scan for it
# with nc -z, then connect. This account just needs a shell; nc is installed.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=knock
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:whosthere" | chpasswd

home="/home/$user"
mkdir -p "$home"
cat > "$home/notes.txt" <<'TEXT'
The doorbell is at the address "doorbell" on this network.
It answers on exactly one port between 5000 and 5999.
After it sends you something, press Ctrl+C to get back to the prompt.
TEXT

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/notes.txt"
