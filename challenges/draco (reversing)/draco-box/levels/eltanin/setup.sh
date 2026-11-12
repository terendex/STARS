#!/bin/bash
# Eltanin (Easy): the program compares your password with the real one using
# strcmp. ltrace shows that call, real password included.
set -euo pipefail

user=eltanin
FLAG='STARS{3lt4n1n_w4tch3s_th3_c4lls}'
PASSWORD='eye-of-the-dragon'
KEY=0x5a

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

# A C array of the text's bytes, each XORed with KEY.
scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

# Not PIE, and lazy binding, because ltrace can't see calls in programs built
# the modern default way.
gcc -O0 -fno-builtin -no-pie -Wl,-z,lazy \
    -DKEY="$KEY" -DPASSWORD_BYTES="$(scrambled "$PASSWORD")" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/eltanin" eltanin.c

# Fail the build unless the password unlocks the flag, a wrong one doesn't,
# and strings shows neither.
printf '%s\n' "$PASSWORD" | "$home/eltanin" | grep -qF "$FLAG"
if printf 'wrong\n' | "$home/eltanin" | grep -qF STARS; then echo "eltanin accepts a wrong password" >&2; exit 1; fi
if strings "$home/eltanin" | grep -qF -e "$PASSWORD" -e STARS; then echo "strings finds eltanin's secrets" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/eltanin"
