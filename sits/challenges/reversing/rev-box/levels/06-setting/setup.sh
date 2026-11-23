#!/bin/bash
# Setting (Easy): the program reads its code from an environment variable.
# ltrace shows the getenv call (the variable's name), then the strcmp call (the
# value it wants).
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=setting
FLAG='FLAG{3nv1r0nm3nt_s3tt1ng_f0und}'
SECRET='midnight-snack'
KEY=0x2d

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -fno-builtin -no-pie -Wl,-z,lazy \
    -DKEY="$KEY" -DSECRET_BYTES="$(scrambled "$SECRET")" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/pantry" pantry.c

PANTRY_CODE="$SECRET" "$home/pantry" | grep -qF "$FLAG"
if "$home/pantry" | grep -qF 'FLAG{'; then echo "pantry prints its flag with no setting" >&2; exit 1; fi
if PANTRY_CODE=wrong "$home/pantry" | grep -qF 'FLAG{'; then echo "pantry accepts a wrong setting" >&2; exit 1; fi
if strings "$home/pantry" | grep -qF -e "$SECRET" -e 'FLAG{'; then echo "strings finds pantry's secrets" >&2; exit 1; fi
strings "$home/pantry" | grep -qF PANTRY_CODE

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/pantry"
