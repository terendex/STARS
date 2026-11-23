#!/bin/bash
# Level Up (Medium): the flag is only shown when a variable is 9000 or more, and
# the program always sets it to 1. Players change it in gdb with `set var`.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=levelup
FLAG='FLAG{1ts_0v3r_n1n3_th0us4nd}'
KEY=0x21

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" -o "$home/game" game.c

if "$home/game" | grep -qF 'FLAG{'; then echo "game prints its flag" >&2; exit 1; fi
if strings "$home/game" | grep -qF 'FLAG{'; then echo "strings finds the flag" >&2; exit 1; fi
gdb -q -batch -ex 'break check_level' -ex run -ex 'set var level = 9000' -ex continue "$home/game" 2>&1 | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/game"
