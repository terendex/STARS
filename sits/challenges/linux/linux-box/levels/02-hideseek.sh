#!/bin/bash
# Hide and Seek (Easy): hidden twice. The flag is a dotfile inside a dot-folder,
# so players need ls -a, then cd, then ls -a again.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=hideseek
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:countto10" | chpasswd

home="/home/$user"
mkdir -p "$home/.closet"

cat > "$home/README.txt" <<'TEXT'
Ready or not, here I come!

The best hiding places don't show up unless you ask to see everything.
And when you find one, look inside it the same way.
TEXT
echo 'Just coats in here. Some names start with a dot, remember?' > "$home/.closet/coats.txt"
echo 'FLAG{y0u_f0und_m3_1n_th3_cl0s3t}' > "$home/.closet/.behind_the_shoes"

chown -R "root:$user" "$home"
find "$home" -type d -exec chmod 750 {} +
find "$home" -type f -exec chmod 640 {} +

# Fail the build unless a plain ls hides both, and ls -a shows each in turn.
[ "$(ls "$home")" = "README.txt" ]
ls -a "$home" | grep -qx '.closet'
[ "$(ls "$home/.closet")" = "coats.txt" ]
ls -a "$home/.closet" | grep -qx '.behind_the_shoes'
