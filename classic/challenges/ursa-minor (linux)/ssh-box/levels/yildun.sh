#!/bin/bash
# Yildun: the flag is in a folder tree, so players have to learn cd and ls.
set -euo pipefail

user=yildun
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:littledipper" | chpasswd

home="/home/$user"
target="$home/sky/northern/ursa-minor/yildun"
mkdir -p "$target" \
    "$home/sky/northern/ursa-major/dubhe" \
    "$home/sky/northern/ursa-minor/polaris" \
    "$home/sky/southern/crux/acrux"

echo 'Nothing recorded here. Keep looking.' | tee \
    "$home/sky/northern/ursa-major/dubhe/notes.txt" \
    "$home/sky/northern/ursa-minor/polaris/notes.txt" \
    "$home/sky/southern/crux/acrux/notes.txt" > /dev/null
echo 'STARS{y1ldun_f0ll0w_th3_p4th}' > "$target/flag.txt"

chown -R "root:$user" "$home"
find "$home" -type d -exec chmod 750 {} +
find "$home" -type f -exec chmod 640 {} +
