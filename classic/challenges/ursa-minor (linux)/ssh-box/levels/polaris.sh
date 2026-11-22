#!/bin/bash
# Polaris: the flag is a dotfile in the home directory.
set -euo pipefail

user=polaris
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:northstar" | chpasswd

home="/home/$user"
mkdir -p "$home"

cat > "$home/README.txt" <<'EOF'
Sailors have steered by the North Star for centuries, but it isn't the
brightest thing in the sky. A lot of what's up there doesn't show up
unless you ask to see all of it.
EOF
echo 'STARS{p0l4r1s_gu1d3s_th3_w4y}' > "$home/.north_star"

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/README.txt" "$home/.north_star"
