#!/bin/bash
# Yildun: one file somewhere in a big folder tree. Walking it with cd and ls
# works but is slow; find does it in one go.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=yildun
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:littlebear" | chpasswd

home="/home/$user"
FLAG='STARS{y1ldun_f0und_1n_th3_4rch1v3}'
target="$home/archive/2025/autumn/northern/little-dipper/yildun"

# Decoy folders: every season of two years, each with a few constellations.
for year in 2024 2025; do
    for season in spring summer autumn winter; do
        for place in northern/little-dipper/polaris northern/little-dipper/kochab northern/draco/thuban \
                     southern/crux/acrux southern/carina/canopus equator/orion/rigel; do
            mkdir -p "$home/archive/$year/$season/$place"
            echo 'Nothing recorded here. Keep looking.' > "$home/archive/$year/$season/$place/notes.txt"
        done
    done
done
mkdir -p "$target"
echo 'Yildun log, autumn 2025.' > "$target/notes.txt"
echo "$FLAG" > "$target/star_record.txt"

chown -R "root:$user" "$home"
find "$home" -type d -exec chmod 750 {} +
find "$home" -type f -exec chmod 640 {} +

# Fail the build if there isn't exactly one star_record.txt.
[ "$(find "$home" -name star_record.txt | wc -l)" -eq 1 ]
grep -qxF "$FLAG" "$(find "$home" -name star_record.txt)"
