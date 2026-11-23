#!/bin/bash
# Welcome Mat (Easy, start here): log in, list the files, read one.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=welcome
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:doormat" | chpasswd

home="/home/$user"
mkdir -p "$home"
cat > "$home/hello.txt" <<'TEXT'
Welcome to the SITS Capture The Flag Competition 2026!
Every flag looks like this one. Copy it into the box on the challenge page.

FLAG{w3lc0m3_t0_th3_sh3ll}
TEXT

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/hello.txt"
