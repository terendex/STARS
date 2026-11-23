#!/bin/bash
# Strings Attached (Easy, start here): the flag is stored in the program as
# plain text. strings finds it.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=strings
FLAG='FLAG{str1ngs_sp1ll_th3_b34ns}'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

gcc -O0 -DFLAG="\"$FLAG\"" -o "$home/secret" secret.c

# Fail the build unless strings shows the flag and running the program doesn't.
strings "$home/secret" | grep -qxF "$FLAG"
if "$home/secret" | grep -qF 'FLAG{'; then echo "secret prints its flag" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/secret"
