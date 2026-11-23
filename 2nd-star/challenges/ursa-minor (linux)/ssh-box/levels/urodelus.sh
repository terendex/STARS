#!/bin/bash
# Urodelus: every reading in the log is repeated a few times, but the real flag
# was logged more often than any other. Each line also has its own time and
# sensor, so players have to pull out the reading before sort and uniq -c can
# count anything. uniq -u (the trick from the first orientation) finds nothing.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=urodelus
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:handlebar" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='STARS{ur0d3lus_h34rd_1t_m0st}'
FLAG_COPIES=11
RANDOM=2026
lines=$(mktemp)
for (( i = 0; i < 1200; i++ )); do
    # Fakes have the same shape as the real flag, so grep can't pick it out.
    s=$(head -c 300 /dev/urandom | tr -dc 'a-z0-9')
    fake="STARS{${s:0:8}_${s:8:5}_${s:13:2}_${s:15:4}}"
    copies=$(( 2 + RANDOM % 6 ))
    for (( n = 0; n < copies; n++ )); do
        echo "$fake" >> "$lines"
    done
done
for (( n = 0; n < FLAG_COPIES; n++ )); do
    echo "$FLAG" >> "$lines"
done
shuf "$lines" \
    | awk 'BEGIN { srand(2026) } { printf "%02d:%02d:%02d dome-%d %s\n", rand() * 24, rand() * 60, rand() * 60, 1 + rand() * 9, $0 }' \
    | sort > "$home/sky.log"
rm "$lines"

# Fail the build if the challenge doesn't have exactly one answer, or if the
# old uniq -u trick finds anything.
counts=$(cut -d' ' -f3 "$home/sky.log" | sort | uniq -c | sort -rn)
[ "$(awk 'NR == 1 { print $2 }' <<< "$counts")" = "$FLAG" ]
[ "$(awk 'NR == 2 { print $1 }' <<< "$counts")" -lt "$FLAG_COPIES" ]
[ -z "$(cut -d' ' -f3 "$home/sky.log" | sort | uniq -u)" ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/sky.log"
