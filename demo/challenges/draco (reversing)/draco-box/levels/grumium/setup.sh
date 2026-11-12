#!/bin/bash
# Grumium (demo, Easy): the flag is stored in the program as plain text. strings finds it.
set -euo pipefail

user=grumium
FLAG='STARS{grum1um_k33ps_1t_1ns1d3}'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

gcc -O0 -DFLAG="\"$FLAG\"" -o "$home/grumium" grumium.c

# Fail the build unless strings shows the flag and running the program doesn't.
strings "$home/grumium" | grep -qxF "$FLAG"
if "$home/grumium" | grep -qF STARS; then echo "grumium prints its flag" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/grumium"
