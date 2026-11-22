#!/bin/bash
# Tyl (Medium): the flag is only shown when a variable is 9000 or more, and the
# program always sets it to 1. Players change it in gdb with `set var`.
set -euo pipefail

user=tyl
FLAG='STARS{tyl_l3v3l3d_up_w1th_gdb}'
KEY=0x15

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/tyl" tyl.c

# Fail the build if running the program or strings shows the flag, or if the
# gdb steps from the answer sheet don't.
if "$home/tyl" | grep -qF STARS; then echo "tyl prints its flag" >&2; exit 1; fi
if strings "$home/tyl" | grep -qF STARS; then echo "strings finds tyl's flag" >&2; exit 1; fi
gdb -q -batch -ex 'break check_level' -ex run -ex 'set var level = 9000' -ex continue "$home/tyl" 2>&1 | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/tyl"
