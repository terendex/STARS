#!/bin/bash
# Russian Doll (Hard): five layers. Unwrapped from the outside: gzip, Base64,
# gzip again, a tar archive, and a Base64 file holding the flag. file says what
# each layer is.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=russiandoll
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:matryoshka" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='FLAG{0p3n3d_3v3ry_s1ngl3_d0ll}'
work=$(mktemp -d)
echo "$FLAG" | base64 > "$work/smallest_doll.txt"
tar -C "$work" -cf - smallest_doll.txt | gzip | base64 | gzip > "$home/doll.dat"
rm -rf "$work"

# Fail the build unless the layers unwrap back to the flag, and file names each
# layer the way the answer key says.
[ "$(gunzip -c "$home/doll.dat" | base64 -d | gunzip | tar -xO | base64 -d)" = "$FLAG" ]
file "$home/doll.dat" | grep -q 'gzip compressed'
gunzip -c "$home/doll.dat" | file - | grep -q 'ASCII text'
gunzip -c "$home/doll.dat" | base64 -d | file - | grep -q 'gzip compressed'
gunzip -c "$home/doll.dat" | base64 -d | gunzip | file - | grep -q 'tar archive'

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/doll.dat"
