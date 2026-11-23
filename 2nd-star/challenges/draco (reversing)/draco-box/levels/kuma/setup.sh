#!/bin/bash
# Kuma (Easy): the program reads its password from an environment variable.
# ltrace shows the getenv call (the variable's name), then the strcmp call (the
# value it wants).
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=kuma
FLAG='STARS{kum4_r34d_1ts_3nv1r0nm3nt}'
SECRET='wake-the-dragon'
KEY=0x29

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

# Not PIE, and lazy binding, because ltrace can't see calls in programs built
# the modern default way.
gcc -O0 -fno-builtin -no-pie -Wl,-z,lazy \
    -DKEY="$KEY" -DSECRET_BYTES="$(scrambled "$SECRET")" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/kuma" kuma.c

# Fail the build unless the setting unlocks the flag, no setting or a wrong one
# doesn't, and strings shows neither secret.
KUMA_EYE="$SECRET" "$home/kuma" | grep -qF "$FLAG"
if "$home/kuma" | grep -qF STARS; then echo "kuma prints its flag with no setting" >&2; exit 1; fi
if KUMA_EYE=wrong "$home/kuma" | grep -qF STARS; then echo "kuma accepts a wrong setting" >&2; exit 1; fi
if strings "$home/kuma" | grep -qF -e "$SECRET" -e STARS; then echo "strings finds kuma's secrets" >&2; exit 1; fi
strings "$home/kuma" | grep -qF KUMA_EYE

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/kuma"
