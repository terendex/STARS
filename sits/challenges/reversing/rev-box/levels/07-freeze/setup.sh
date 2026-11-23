#!/bin/bash
# Freeze Frame (Medium): the flag only exists in memory, between write_note()
# and burn_note(). Players stop the program in gdb and read it.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=freeze
FLAG='FLAG{c4ught_b3f0r3_th3_burn}'
KEY=0x37

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -Wl,-z,lazy -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/notes" notes.c

if "$home/notes" | grep -qF 'FLAG{'; then echo "notes prints its flag" >&2; exit 1; fi
if strings "$home/notes" | grep -qF 'FLAG{'; then echo "strings finds the flag" >&2; exit 1; fi
gdb -q -batch -ex 'break burn_note' -ex run -ex 'info args' "$home/notes" 2>&1 | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/notes"
