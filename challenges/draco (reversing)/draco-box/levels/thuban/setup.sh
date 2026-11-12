#!/bin/bash
# Thuban (Easy): the flag is stored in the program as plain text. strings finds it.
set -euo pipefail

user=thuban
FLAG='STARS{thub4n_th3_0ld_p0l3_st4r}'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

gcc -O0 -DFLAG="\"$FLAG\"" -o "$home/thuban" thuban.c

# Fail the build unless strings shows the flag and running the program doesn't.
strings "$home/thuban" | grep -qxF "$FLAG"
if "$home/thuban" | grep -qF STARS; then echo "thuban prints its flag" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/thuban"
