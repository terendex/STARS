#!/bin/bash
# Pherkad: the very first step. Log in, list the files, read one.
set -euo pipefail

user=pherkad
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:firststep" | chpasswd

home="/home/$user"
mkdir -p "$home"
echo 'STARS{ph3rk4d_f1rst_st3p}' > "$home/flag.txt"

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/flag.txt"
