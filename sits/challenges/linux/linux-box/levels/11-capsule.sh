#!/bin/bash
# Time Capsule (Medium): 366 diary pages with random names, one for every day of
# 2024. Each holds a flag-shaped line, but only the page last changed on
# 14 February 2024 holds the real one. Players find it by date (ls -l or find).
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=capsule
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:buriedtreasure" | chpasswd

home="/home/$user"
diary="$home/diary"
mkdir -p "$diary"

FLAG='FLAG{d4t3d_v4l3nt1n3s_d4y}'
TARGET='2024-02-14'
RANDOM=214
for (( day = 0; day < 366; day++ )); do
    date=$(date -u -d "2024-01-01 + $day days" +%F)
    name="page-$(head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n').txt"
    if [ "$date" = "$TARGET" ]; then
        flag=$FLAG
    else
        flag="FLAG{$(head -c 300 /dev/urandom | tr -dc 'a-z0-9' | head -c 20)}"
    fi
    printf 'Dear diary,\nmood: %d/10\nsecret: %s\n' $(( 1 + RANDOM % 10 )) "$flag" > "$diary/$name"
    touch -d "$date $(printf '%02d:%02d' $(( 18 + RANDOM % 5 )) $(( RANDOM % 60 ))):00 UTC" "$diary/$name"
done

chown -R "root:$user" "$home"
chmod 750 "$home" "$diary"
chmod 640 "$diary"/*

# Fail the build unless exactly one page was changed that day, and it has the flag.
[ "$(find "$diary" -type f -newermt "$TARGET 00:00 UTC" ! -newermt "$TARGET 23:59:59 UTC" | wc -l)" -eq 1 ]
grep -qF "$FLAG" "$(find "$diary" -type f -newermt "$TARGET 00:00 UTC" ! -newermt "$TARGET 23:59:59 UTC")"
