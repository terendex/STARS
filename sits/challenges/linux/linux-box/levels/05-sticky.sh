#!/bin/bash
# Sticky Note (Easy): the flag isn't in a file. sshd sets it as an environment
# variable when this account logs in, among a few ordinary-looking ones.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=sticky
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:postit" | chpasswd

home="/home/$user"
mkdir -p "$home"
cat > "$home/notes.txt" <<'TEXT'
I didn't write the reminder in a file this time.
It's stuck to your session: you get it the moment you log in.
TEXT

FLAG='FLAG{st1cky_n0t3_1n_th3_3nv}'
# A Match block, so only this account gets these. Match blocks run to the end of
# the file, which is why every level adds its own at the end.
cat >> /etc/ssh/sshd_config <<CONF

Match User $user
    SetEnv FAVOURITE_SNACK=popcorn LUNCH_AT=12:30 REMINDER=$FLAG WIFI_ROOM=library
CONF

grep -qF "REMINDER=$FLAG" /etc/ssh/sshd_config

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/notes.txt"
