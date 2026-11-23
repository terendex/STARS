#!/bin/bash
# Read the Assembly (Medium): the code is a number inside a cmp instruction, so
# strings can't find it. Players read it from `disassemble check_code` in gdb.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=assembly
FLAG='FLAG{1t_w4s_1n_th3_4ss3mbly}'
CODE=0x7b2d1
KEY=0x59

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -fno-builtin -no-pie -DCODE="${CODE}L" -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/vault" vault.c

echo "$CODE" | "$home/vault" | grep -qF "$FLAG"
echo "$((CODE))" | "$home/vault" | grep -qF "$FLAG"
if echo 12345 | "$home/vault" | grep -qF 'FLAG{'; then echo "vault accepts a wrong code" >&2; exit 1; fi
if strings "$home/vault" | grep -qF 'FLAG{'; then echo "strings finds the flag" >&2; exit 1; fi
gdb -q -batch -ex 'disassemble check_code' "$home/vault" 2>&1 | grep cmp | grep -qF "\$$CODE,"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/vault"
