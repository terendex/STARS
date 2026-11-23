#!/bin/bash
# Spot the Difference (Easy): two guest lists, identical except for one line.
# Every line has a code that looks like a flag, so grep can't help; diff finds
# the changed line at once.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=spotdiff
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:twinphotos" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='FLAG{0n3_l1n3_ch4ng3d}'
CHANGED=2214
names=(Ana Ben Carlo Dana Eli Faye Gino Hana Ivan Jade Kiko Lia Migo Nina Oli Pia)
old="$home/guests-monday.txt"
new="$home/guests-friday.txt"
: > "$old"
: > "$new"
for (( i = 1; i <= 3000; i++ )); do
    code="FLAG{$(head -c 9 /dev/urandom | od -An -tx1 | tr -d ' \n')}"
    line=$(printf 'guest %04d  %-6s  table %02d  ticket %s' "$i" "${names[i % 16]}" $(( 1 + i % 40 )) "$code")
    echo "$line" >> "$old"
    if (( i == CHANGED )); then
        printf 'guest %04d  %-6s  table %02d  ticket %s\n' "$i" "${names[i % 16]}" $(( 1 + i % 40 )) "$FLAG" >> "$new"
    else
        echo "$line" >> "$new"
    fi
done

# Fail the build unless diff shows exactly one changed line, holding the flag.
[ "$({ diff "$old" "$new" || true; } | grep -c '^>')" -eq 1 ]
{ diff "$old" "$new" || true; } | grep '^>' | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$old" "$new"
