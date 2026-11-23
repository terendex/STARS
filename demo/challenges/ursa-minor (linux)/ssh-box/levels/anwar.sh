#!/bin/bash
# Anwar: the flag is in a file whose name has spaces in it.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=anwar
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:farkadain" | chpasswd

home="/home/$user"
mkdir -p "$home"
echo 'STARS{4nw4r_qu0t3s_th3_sp4c3s}' > "$home/anwar al farkadain.txt"

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/anwar al farkadain.txt"
