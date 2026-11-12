#!/bin/bash
# Altais (Medium): the flag only exists in memory, between remember_flag() and
# forget_flag(). Players stop the program in gdb and read it.
set -euo pipefail

user=altais
FLAG='STARS{4lt41s_c4ught_1n_m3m0ry}'
KEY=0x2c

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -Wl,-z,lazy -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/altais" altais.c

# Fail the build if running the program or strings shows the flag.
if "$home/altais" | grep -qF STARS; then echo "altais prints its flag" >&2; exit 1; fi
if strings "$home/altais" | grep -qF STARS; then echo "strings finds altais's flag" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/altais"
