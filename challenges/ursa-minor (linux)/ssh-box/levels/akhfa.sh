#!/bin/bash
# Akhfa: the flag is gzipped, then put in a tar, gzipped again, and Base64 encoded.
set -euo pipefail

user=akhfa
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:hiddenstar" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='STARS{4khf4_unwr4pp3d_4t_l4st}'
work=$(mktemp -d)
echo "$FLAG" | gzip > "$work/transmission.gz"
tar -C "$work" -cf - transmission.gz | gzip | base64 > "$home/signal.dat"
rm -rf "$work"

# Fail the build if the layers don't unwrap back to the flag.
[ "$(base64 -d "$home/signal.dat" | gunzip | tar -xO | gunzip)" = "$FLAG" ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/signal.dat"
