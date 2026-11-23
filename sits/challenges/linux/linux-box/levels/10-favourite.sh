#!/bin/bash
# Crowd Favourite (Medium): every vote in the log was cast a few times, but the
# winning one more often than any other. Players cut out the vote, then count
# with sort, uniq -c and sort -n.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=favourite
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:mostvotes" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='FLAG{th3_cr0wd_h4s_sp0k3n}'
WINS=14
RANDOM=2026
lines=$(mktemp)
for (( i = 0; i < 1000; i++ )); do
    s=$(head -c 300 /dev/urandom | tr -dc 'a-z0-9')
    fake="FLAG{${s:0:5}_${s:5:4}_${s:9:6}}"
    for (( n = 0; n < 2 + RANDOM % 8; n++ )); do echo "$fake" >> "$lines"; done
done
for (( n = 0; n < WINS; n++ )); do echo "$FLAG" >> "$lines"; done
shuf "$lines" \
    | awk 'BEGIN { srand(14) } { printf "%02d:%02d booth-%d %s\n", rand() * 24, rand() * 60, 1 + rand() * 8, $0 }' \
    | sort > "$home/votes.log"
rm "$lines"

# Fail the build unless the most counted vote is the flag, clearly ahead.
counts=$(cut -d' ' -f3 "$home/votes.log" | sort | uniq -c | sort -rn)
[ "$(awk 'NR == 1 { print $2 }' <<< "$counts")" = "$FLAG" ]
[ "$(awk 'NR == 2 { print $1 }' <<< "$counts")" -lt "$WINS" ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/votes.log"
