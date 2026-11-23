#!/bin/bash
# Odd One Out (Medium): every sock in the laundry log has a matching pair, except
# one. Each line has its own time and basket, so players cut out the sock code
# before sort and uniq -u can find the one that appears once.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=oddone
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:pairsonly" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='FLAG{th3_l0n3ly_s0ck}'
lines=$(mktemp)
for (( i = 0; i < 1500; i++ )); do
    s=$(head -c 300 /dev/urandom | tr -dc 'a-z0-9')
    fake="FLAG{${s:0:3}_${s:3:6}_${s:9:4}}"
    echo "$fake" >> "$lines"
    echo "$fake" >> "$lines"
done
echo "$FLAG" >> "$lines"
shuf "$lines" \
    | awk 'BEGIN { srand(1500) } { printf "%02d:%02d basket-%d sock %s\n", rand() * 24, rand() * 60, 1 + rand() * 6, $0 }' \
    | sort > "$home/laundry.log"
rm "$lines"

# Fail the build unless uniq -u on the sock column gives exactly the flag, and
# uniq -u on whole lines gives thousands of lines (so cut is needed).
[ "$(cut -d' ' -f4 "$home/laundry.log" | sort | uniq -u)" = "$FLAG" ]
[ "$(sort "$home/laundry.log" | uniq -u | wc -l)" -gt 2000 ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/laundry.log"
