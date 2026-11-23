#!/bin/bash
# License Key (Hard): a valid key is any 8 digits that add up to 42. The
# messages say which rule a key broke; the disassembly of check_key shows the
# rules, including the total, 0x2a.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=license
FLAG='FLAG{m4d3_my_0wn_k3yg3n}'
TOTAL=42
KEY=0x46

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -Wl,-z,lazy -DTOTAL="$TOTAL" -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/license" license.c

# Fail the build unless any 8 digits adding up to 42 work, and each kind of
# wrong key gets its own message.
for key in 99996000 66666660 00099996 77777700; do
    echo "$key" | "$home/license" | grep -qF "$FLAG"
done
echo 1234567 | "$home/license" | grep -qF '8 characters'
echo 9999600a | "$home/license" | grep -qF 'only digits'
echo 99996001 | "$home/license" | grep -qF 'add up'
if strings "$home/license" | grep -qF 'FLAG{'; then echo "strings finds the flag" >&2; exit 1; fi
gdb -q -batch -ex 'disassemble check_key' "$home/license" 2>&1 | grep cmp | grep -qF '$0x2a,'

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/license"
