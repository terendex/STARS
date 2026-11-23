#!/bin/bash
# Skip the Wait (Medium): the program sleeps for a thousand years before it
# prints the flag. Players leave the waiting function early in gdb with return.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=skipwait
FLAG='FLAG{sk1pp3d_th3_wh0l3_qu3u3}'
KEY=0x63

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -Wl,-z,lazy -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" -o "$home/queue" queue.c

if strings "$home/queue" | grep -qF 'FLAG{'; then echo "strings finds the flag" >&2; exit 1; fi
gdb -q -batch -ex 'break wait_in_line' -ex run -ex return -ex continue "$home/queue" 2>&1 | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/queue"
