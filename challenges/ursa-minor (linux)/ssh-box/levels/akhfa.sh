#!/bin/bash
# Akhfa: five layers. Unwrapped from the outside: Base64, gzip, Base64 again,
# a tar archive, and a gzipped file holding the flag.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=akhfa
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:dimmerstar" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='STARS{4khf4_p33l3d_3v3ry_l4y3r}'
work=$(mktemp -d)
echo "$FLAG" | gzip > "$work/core.gz"
tar -C "$work" -cf - core.gz | base64 | gzip | base64 > "$home/signal.dat"
rm -rf "$work"

# Fail the build if the layers don't unwrap back to the flag.
[ "$(base64 -d "$home/signal.dat" | gunzip | base64 -d | tar -xO | gunzip)" = "$FLAG" ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/signal.dat"
