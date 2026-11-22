#!/bin/bash
# Urodelus: every reading in the log is repeated except the real flag, but each
# line also has its own time and sensor, so players have to pull out the reading
# before sort and uniq can compare anything.
set -euo pipefail

user=urodelus
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:dipperhandle" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='STARS{ur0d3lus_0n3_0f_4_k1nd}'
RANDOM=2024
lines=$(mktemp)
for (( i = 0; i < 1500; i++ )); do
    # Fakes have the same shape as the real flag, so grep can't pick it out.
    s=$(head -c 300 /dev/urandom | tr -dc 'a-z0-9')
    fake="STARS{${s:0:8}_${s:8:3}_${s:11:2}_${s:13:1}_${s:14:4}}"
    copies=$(( 2 + RANDOM % 3 ))
    for (( n = 0; n < copies; n++ )); do
        echo "$fake" >> "$lines"
    done
done
echo "$FLAG" >> "$lines"
shuf "$lines" \
    | awk 'BEGIN { srand(2024) } { printf "%02d:%02d:%02d dome-%d %s\n", rand() * 24, rand() * 60, rand() * 60, 1 + rand() * 9, $0 }' \
    | sort > "$home/sky.log"
rm "$lines"

# Fail the build if the challenge doesn't have exactly one answer.
[ "$(cut -d' ' -f3 "$home/sky.log" | sort | uniq -u)" = "$FLAG" ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/sky.log"
