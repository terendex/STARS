#!/bin/bash
# Compare Notes (Easy): the program compares your password with the real one
# using strcmp. ltrace shows that call, real password included.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=compare
FLAG='FLAG{ltr4c3_s4w_th3_c0mp4r3}'
PASSWORD='pineapple-on-pizza'
KEY=0x4b

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

# Not PIE, and lazy binding, because ltrace can't see calls in programs built
# the modern default way.
gcc -O0 -fno-builtin -no-pie -Wl,-z,lazy \
    -DKEY="$KEY" -DPASSWORD_BYTES="$(scrambled "$PASSWORD")" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/checker" checker.c

"$home/checker" "$PASSWORD" | grep -qF "$FLAG"
if "$home/checker" wrong | grep -qF 'FLAG{'; then echo "checker accepts a wrong password" >&2; exit 1; fi
if strings "$home/checker" | grep -qF -e "$PASSWORD" -e 'FLAG{'; then echo "strings finds checker's secrets" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/checker"
