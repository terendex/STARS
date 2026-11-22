#!/bin/bash
# Lambda: two copies of a catalog, identical except for one line. Every line has
# a fake flag, so grep can't help; diff finds the changed line at once.
set -euo pipefail

user=lambda
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:twocopies" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='STARS{l4mbd4_sp0tt3d_th3_d1ff3r3nc3}'
CHANGED=1377
RANDOM=777
old="$home/catalog-old.txt"
new="$home/catalog-new.txt"
: > "$old"
: > "$new"
for (( i = 1; i <= 2400; i++ )); do
    code="STARS{$(head -c 10 /dev/urandom | od -An -tx1 | tr -d ' \n')}"
    line=$(printf 'HIP %06d  mag %d.%02d  code %s' $(( 1000 + i * 37 )) $(( RANDOM % 7 )) $(( RANDOM % 100 )) "$code")
    echo "$line" >> "$old"
    if (( i == CHANGED )); then
        printf 'HIP %06d  mag %d.%02d  code %s\n' $(( 1000 + i * 37 )) 4 7 "$FLAG" >> "$new"
    else
        echo "$line" >> "$new"
    fi
done

# Fail the build unless diff shows exactly one changed line holding the flag.
[ "$(diff "$old" "$new" | grep -c '^>')" -eq 1 ]
diff "$old" "$new" | grep '^>' | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$old" "$new"
