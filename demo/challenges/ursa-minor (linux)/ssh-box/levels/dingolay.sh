#!/bin/bash
# Dingolay: one line in a 20,000-line log holds the flag. grep finds it.
set -euo pipefail

user=dingolay
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:ramajay" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='STARS{d1ng0l4y_n33dl3_1n_th3_l0g}'
LINES=20000
FLAG_LINE=13417
RANDOM=11

for (( i = 1; i <= LINES; i++ )); do
    printf '2026-11-%02d %02d:%02d:%02d  sensor-%02d  magnitude %d.%02d  status ok' \
        $(( 1 + (i - 1) * 30 / LINES )) $(( RANDOM % 24 )) $(( RANDOM % 60 )) $(( RANDOM % 60 )) \
        $(( 1 + RANDOM % 12 )) $(( 4 + RANDOM % 3 )) $(( RANDOM % 100 ))
    (( i == FLAG_LINE )) && printf '  note: %s' "$FLAG"
    printf '\n'
done > "$home/sky_survey.log"

# Fail the build unless exactly one line has the flag.
[ "$(grep -c 'STARS{' "$home/sky_survey.log")" -eq 1 ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/sky_survey.log"
