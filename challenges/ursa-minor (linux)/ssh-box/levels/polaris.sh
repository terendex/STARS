#!/bin/bash
# Polaris: hidden twice. The record is a dotfile inside a dot-folder, so players
# need ls -a, then cd, then ls -a again.
set -euo pipefail

user=polaris
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:polestar" | chpasswd

home="/home/$user"
mkdir -p "$home/.observatory"

cat > "$home/README.txt" <<'TEXT'
Sailors have steered by the North Star for centuries, but it isn't the
brightest thing in the sky. A lot of what's up there doesn't show up
unless you ask to see all of it.

And whatever you find might be a place you can go into, with more
hiding inside.
TEXT
echo 'Not this one. Look closer: some names in here start with a dot.' > "$home/.observatory/notes.txt"
echo 'STARS{p0l4r1s_h1d1ng_1n_pl41n_s1ght}' > "$home/.observatory/.pole_record"

chown -R "root:$user" "$home"
find "$home" -type d -exec chmod 750 {} +
find "$home" -type f -exec chmod 640 {} +

# Fail the build if ls -a in the hidden folder doesn't show the record.
[ "$(ls -a "$home/.observatory" | grep -c '^\.pole_record$')" -eq 1 ]
[ -z "$(ls "$home" | grep observatory || true)" ]
