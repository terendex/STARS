#!/bin/bash
# Aldhibah (Hard): the program sleeps for a thousand years, then only prints the
# flag for root. Players skip both in gdb with `return`.
set -euo pipefail

user=aldhibah
FLAG='STARS{4ldh1b4h_w0k3_th3_dr4g0n}'
KEY=0x71

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -Wl,-z,lazy -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/aldhibah" aldhibah.c

# Fail the build if strings shows the flag.
if strings "$home/aldhibah" | grep -qF STARS; then echo "strings finds aldhibah's flag" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/aldhibah"
