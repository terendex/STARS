#!/bin/bash
# Fafnir (Hard): the program only prints the flag when it's started under its
# true name. ltrace shows the strcmp with the true name in it, and then
# players start it under that name, with ln -s or exec -a.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=fafnir
FLAG='STARS{f4fn1r_4nsw3rs_t0_h1s_tru3_n4m3}'
TRUE_NAME='gnitaheath-wyrm'
KEY=0x5a

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

# C arrays of the bytes: the true name XORed with KEY, and the flag XORed with
# the true name (repeated), so only the true name can unlock it.
name_bytes=$(python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$TRUE_NAME" "$KEY")
flag_bytes=$(python3 -c 'import sys; f, n = sys.argv[1], sys.argv[2]; print("{" + ",".join(hex(ord(c) ^ ord(n[i % len(n)])) for i, c in enumerate(f)) + "}")' "$FLAG" "$TRUE_NAME")

# Not PIE, and lazy binding, because ltrace can't see calls in programs built
# the modern default way.
gcc -O0 -fno-builtin -no-pie -Wl,-z,lazy \
    -DKEY="$KEY" -DNAME_BYTES="$name_bytes" -DFLAG_BYTES="$flag_bytes" \
    -o "$home/fafnir" fafnir.c

# Fail the build unless its own name is refused, the true name works both ways
# players will try, strings finds neither secret, and ltrace shows the name.
if "$home/fafnir" | grep -qF 'STARS{'; then echo "fafnir gives the flag to anyone" >&2; exit 1; fi
(exec -a "$TRUE_NAME" "$home/fafnir") | grep -qF "$FLAG"
ln -s "$home/fafnir" "/tmp/$TRUE_NAME"
"/tmp/$TRUE_NAME" | grep -qF "$FLAG"
rm "/tmp/$TRUE_NAME"
if strings "$home/fafnir" | grep -qF -e "$TRUE_NAME" -e 'STARS{'; then echo "strings finds fafnir's secrets" >&2; exit 1; fi
ltrace "$home/fafnir" 2>&1 | grep -qF "\"$TRUE_NAME\""

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/fafnir"
