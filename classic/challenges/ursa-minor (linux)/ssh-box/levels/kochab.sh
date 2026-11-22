#!/bin/bash
# Kochab: one real record among hundreds of decoys. Every decoy carries a fake
# flag, so a plain grep isn't enough: players have to filter by size and owner.
set -euo pipefail

user=kochab
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:guardian" | chpasswd
useradd -M -s /usr/sbin/nologin astronomer

home="/home/$user"
catalog="$home/catalog"
mkdir -p "$catalog"

FLAG='STARS{k0ch4b_gu4rd14n_0f_th3_p0l3}'
TARGET_SIZE=1337
TARGET_OWNER=astronomer
RECORDS=600
RANDOM=1337

write_record() {
    local file=$1 owner=$2 size=$3 flag=$4
    local header
    header=$(printf 'HD %s\nflag: %s\nspectrum: ' "$(basename "$file" .rec)" "$flag")
    local pad=$(( size - ${#header} ))
    {
        printf '%s' "$header"
        head -c "$pad" /dev/urandom | base64 -w0 | cut -c1-"$pad" | tr -d '\n'
    } > "$file"
    chown "$owner:$user" "$file"
    chmod 640 "$file"
}

for (( i = 0; i < RECORDS; i++ )); do
    file="$catalog/HD$(( 100000 + i * 137 )).rec"
    fake="STARS{$(head -c 12 /dev/urandom | od -An -tx1 | tr -d ' \n')}"
    owner=root
    size=$(( 900 + RANDOM % 1000 ))
    [ "$size" -eq "$TARGET_SIZE" ] && size=$(( size + 1 ))

    if (( i == 412 )); then
        write_record "$file" "$TARGET_OWNER" "$TARGET_SIZE" "$FLAG"
        continue
    elif (( i % 25 == 0 )); then
        # Right size, wrong owner.
        size=$TARGET_SIZE
    elif (( i % 5 == 0 )); then
        # Right owner, wrong size.
        owner=$TARGET_OWNER
    fi
    write_record "$file" "$owner" "$size" "$fake"
done

# Fail the build if the challenge doesn't have exactly one answer.
matches=$(find "$catalog" -type f -size "${TARGET_SIZE}c" -user "$TARGET_OWNER" | wc -l)
[ "$matches" -eq 1 ]
grep -q "$FLAG" "$(find "$catalog" -type f -size "${TARGET_SIZE}c" -user "$TARGET_OWNER")"

chown "root:$user" "$home" "$catalog"
chmod 750 "$home" "$catalog"
