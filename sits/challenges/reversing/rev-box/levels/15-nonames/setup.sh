#!/bin/bash
# No Names (Hard): a stripped program, so gdb knows none of its own functions.
# It still calls the library's memset to wipe the flag, so players break there
# and print memset's first argument with x/s $rdi.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=nonames
FLAG='FLAG{n0_n4m3s_n0_pr0bl3m}'
KEY=0x6e

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -fno-builtin -no-pie -Wl,-z,lazy -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" -o "$home/nonames" nonames.c
strip "$home/nonames"

# Fail the build unless the program's own names are gone, strings doesn't show
# the flag, and the hint's gdb steps do.
if nm "$home/nonames" 2>&1 | grep -qw -e decode -e wipe -e main; then echo "nonames still has names" >&2; exit 1; fi
if strings "$home/nonames" | grep -qF 'FLAG{'; then echo "strings finds the flag" >&2; exit 1; fi
gdb -q -batch -ex 'break memset' -ex run -ex 'x/s $rdi' "$home/nonames" 2>&1 | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/nonames"
