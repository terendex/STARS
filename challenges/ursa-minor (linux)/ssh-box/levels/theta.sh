#!/bin/bash
# Theta: 365 observation files with random names, one for every night of 2025.
# Each holds a flag-shaped line, but only the file last changed on the night of
# 12 August 2025 holds the real one. Players find it by date (ls -l or find).
set -euo pipefail

user=theta
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:perseids" | chpasswd

home="/home/$user"
obs="$home/observations"
mkdir -p "$obs"

FLAG='STARS{th3t4_c4ught_th3_p3rs31ds}'
TARGET='2025-08-12'
RANDOM=365
for (( day = 0; day < 365; day++ )); do
    date=$(date -u -d "2025-01-01 + $day days" +%F)
    name="obs-$(head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n').log"
    if [ "$date" = "$TARGET" ]; then
        flag=$FLAG
    else
        flag="STARS{$(head -c 300 /dev/urandom | tr -dc 'a-z0-9' | head -c 20)}"
    fi
    printf 'Theta all-sky camera\nframes: %d\nreading: %s\n' $(( 100 + RANDOM % 900 )) "$flag" > "$obs/$name"
    touch -d "$date $(printf '%02d:%02d' $(( 20 + RANDOM % 4 )) $(( RANDOM % 60 ))):00 UTC" "$obs/$name"
done

# Fail the build unless exactly one file was changed on that night, and it has the flag.
[ "$(find "$obs" -type f -newermt "$TARGET 00:00 UTC" ! -newermt "$TARGET 23:59:59 UTC" | wc -l)" -eq 1 ]
match=$(find "$obs" -type f -newermt "$TARGET 00:00 UTC" ! -newermt "$TARGET 23:59:59 UTC")
grep -qF "$FLAG" "$match"

chown -R "root:$user" "$home"
chmod 750 "$home" "$obs"
chmod 640 "$obs"/*
# chown and chmod don't change the modification time, but check anyway.
[ "$(find "$obs" -type f -newermt "$TARGET 00:00 UTC" ! -newermt "$TARGET 23:59:59 UTC")" = "$match" ]
