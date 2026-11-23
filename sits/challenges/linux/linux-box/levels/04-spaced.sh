#!/bin/bash
# Spaced Out (Easy): the flag is in a file whose name has spaces and brackets,
# so typing it plainly fails. Quotes (or Tab to complete the name) fix it.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=spaced
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:spacebar" | chpasswd

home="/home/$user"
mkdir -p "$home"
echo 'Milk, eggs, bread. The flag is in the other list.' > "$home/shopping.txt"
echo 'FLAG{qu0t3s_h4ndl3_sp4c3s}' > "$home/my secret plans (final).txt"

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home"/*

# Fail the build unless the file is readable with quotes, and not without.
grep -q FLAG "$home/my secret plans (final).txt"
if cat $home/my secret plans 2>/dev/null; then echo "the name works without quotes" >&2; exit 1; fi
