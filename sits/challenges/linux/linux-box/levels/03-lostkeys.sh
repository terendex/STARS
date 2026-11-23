#!/bin/bash
# Lost Keys (Easy): one file somewhere in a big folder tree. Walking it with cd
# and ls works but is slow; find does it in one go.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=lostkeys
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:jinglejingle" | chpasswd

home="/home/$user"
FLAG='FLAG{f1nd_f0und_th3_k3ys}'

# Decoy rooms: every room of the house, each with furniture and a note.
for floor in downstairs upstairs basement attic; do
    for room in kitchen bedroom bathroom hallway study garage; do
        for spot in drawer shelf cupboard box under-the-bed; do
            mkdir -p "$home/house/$floor/$room/$spot"
            echo 'Not here. Socks, receipts and a lot of dust.' > "$home/house/$floor/$room/$spot/notes.txt"
        done
    done
done
target="$home/house/upstairs/study/drawer"
echo "$FLAG" > "$target/keys.txt"

chown -R "root:$user" "$home"
find "$home" -type d -exec chmod 750 {} +
find "$home" -type f -exec chmod 640 {} +

# Fail the build unless there's exactly one keys.txt and it holds the flag.
[ "$(find "$home" -name keys.txt | wc -l)" -eq 1 ]
grep -qxF "$FLAG" "$(find "$home" -name keys.txt)"
