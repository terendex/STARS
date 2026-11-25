#!/bin/bash
# Fafnir (Medium): the program only prints the flag when it's started under its
# true name. The true name is plain text inside the program, so strings lists
# it and ltrace shows the strcmp with it. Then players start the program under
# that name, with ln -s or exec -a.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=fafnir
FLAG='STARS{f4fn1r_4nsw3rs_t0_h1s_tru3_n4m3}'
TRUE_NAME='gnitaheath-wyrm'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

# A C array of the flag XORed with the true name (repeated), so only the true
# name can unlock it.
flag_bytes=$(python3 -c 'import sys; f, n = sys.argv[1], sys.argv[2]; print("{" + ",".join(hex(ord(c) ^ ord(n[i % len(n)])) for i, c in enumerate(f)) + "}")' "$FLAG" "$TRUE_NAME")

# Not PIE, and lazy binding, because ltrace can't see calls in programs built
# the modern default way.
gcc -O0 -fno-builtin -no-pie -Wl,-z,lazy \
    -DTRUE_NAME="\"$TRUE_NAME\"" -DFLAG_BYTES="$flag_bytes" \
    -o "$home/fafnir" fafnir.c

# Fail the build unless its own name is refused, the true name works both ways
# players will try, strings finds the true name but not the flag, and ltrace
# shows the name.
if "$home/fafnir" | grep -qF 'STARS{'; then echo "fafnir gives the flag to anyone" >&2; exit 1; fi
(exec -a "$TRUE_NAME" "$home/fafnir") | grep -qF "$FLAG"
ln -s "$home/fafnir" "/tmp/$TRUE_NAME"
"/tmp/$TRUE_NAME" | grep -qF "$FLAG"
rm "/tmp/$TRUE_NAME"
strings "$home/fafnir" | grep -qxF "$TRUE_NAME"
if strings "$home/fafnir" | grep -qF 'STARS{'; then echo "strings finds fafnir's flag" >&2; exit 1; fi
ltrace "$home/fafnir" 2>&1 | grep -qF "\"$TRUE_NAME\""

# Reset this level on logout. The shared /tmp is the only writable place (the
# home is read-only while the box runs), so a link or a stray folder left under
# the true name sticks around and the next player's `ln -s` fails with
# "File exists" or lands inside the folder. bash runs ~/.bash_logout when a
# login shell exits, so clearing this account's own /tmp entries there hands the
# next session a clean slate. Scoped to this user, which is all the sticky /tmp
# lets it remove anyway.
cat > "$home/.bash_logout" <<EOF
# Clear this account's scratch in the shared /tmp when the login shell exits.
find /tmp -mindepth 1 -maxdepth 1 -user $user -exec rm -rf {} + 2>/dev/null
EOF

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/fafnir"
