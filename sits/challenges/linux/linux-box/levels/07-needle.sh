#!/bin/bash
# Needle in the Logs (Medium): 25,000 login records, every one with a token that
# looks like a flag. The flag is the token on the only DENIED login by the user
# "principal", so players chain two greps (or one with both words).
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=needle
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:haystack" | chpasswd

home="/home/$user"
mkdir -p "$home"

FLAG='FLAG{tw0_gr3ps_1n_4_r0w}'
LINES=25000
# Plenty of denied logins, and plenty by the principal, but never both, except
# on the target line.
awk -v lines="$LINES" -v target=17391 -v flag="$FLAG" 'BEGIN {
    srand(7)
    split("ana ben carlo dana eli faye gino hana ivan jade principal kiko lia", people, " ")
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    for (i = 1; i <= lines; i++) {
        who = people[1 + int(rand() * 13)]
        result = (rand() < 0.11) ? "DENIED" : "ok"
        if (who == "principal" && result == "DENIED") result = "ok"
        token = "FLAG{"
        for (k = 0; k < 18; k++) token = token substr(chars, 1 + int(rand() * 36), 1)
        token = token "}"
        if (i == target) { who = "principal"; result = "DENIED"; token = flag }
        printf "2026-03-%02d %02d:%02d:%02d login user=%s result=%s token=%s\n",
            1 + int((i - 1) * 28 / lines), int(rand() * 24), int(rand() * 60), int(rand() * 60), who, result, token
    }
}' > "$home/logins.log"

# Fail the build unless the two-word search finds exactly the flag's line, and
# a search for FLAG alone finds thousands.
[ "$(grep 'user=principal' "$home/logins.log" | grep -c 'DENIED')" -eq 1 ]
grep 'user=principal' "$home/logins.log" | grep DENIED | grep -qF "$FLAG"
[ "$(grep -c 'FLAG{' "$home/logins.log")" -eq "$LINES" ]

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/logins.log"
