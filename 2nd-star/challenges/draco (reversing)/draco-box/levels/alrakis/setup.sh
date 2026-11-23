#!/bin/bash
# Alrakis (Medium): the code is a number inside a cmp instruction, so strings
# can't find it. Players read it from `disassemble check_code` in gdb.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=alrakis
FLAG='STARS{4lr4k1s_r34d_th3_4ss3mbly}'
CODE=0x5e1f3
KEY=0x63

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -fno-builtin -no-pie -DCODE="${CODE}L" -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/alrakis" alrakis.c

# Fail the build unless the code works typed as hex or decimal, a wrong one
# doesn't, strings doesn't show the flag, and the code is in a cmp instruction
# inside check_code.
echo "$CODE" | "$home/alrakis" | grep -qF "$FLAG"
echo "$((CODE))" | "$home/alrakis" | grep -qF "$FLAG"
if echo 12345 | "$home/alrakis" | grep -qF STARS; then echo "alrakis accepts a wrong code" >&2; exit 1; fi
if strings "$home/alrakis" | grep -qF STARS; then echo "strings finds alrakis's flag" >&2; exit 1; fi
objdump -d "$home/alrakis" | sed -n '/<check_code>:/,/ret/p' | grep "cmp" | grep -qF "\$$CODE,"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/alrakis"
