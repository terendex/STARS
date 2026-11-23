#!/bin/bash
# Kochab: one real record among hundreds of decoys, spread over 12 folders.
# Every decoy carries a fake flag, so a plain grep isn't enough: players have
# to filter by size and owner.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=kochab
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:guardians" | chpasswd
useradd -M -s /usr/sbin/nologin cartographer

home="/home/$user"
charts="$home/charts"
mkdir -p "$charts"

FLAG='STARS{k0ch4b_m4pp3d_th3_n0rth}'
TARGET_SIZE=2048
TARGET_OWNER=cartographer
RECORDS=900
RANDOM=2048

write_record() {
    local file=$1 owner=$2 size=$3 flag=$4
    local header
    header=$(printf 'HIP %s\nflag: %s\nchart: ' "$(basename "$file" .chart)" "$flag")
    local pad=$(( size - ${#header} ))
    {
        printf '%s' "$header"
        head -c "$pad" /dev/urandom | base64 -w0 | cut -c1-"$pad" | tr -d '\n'
    } > "$file"
    chown "$owner:$user" "$file"
    chmod 640 "$file"
}

for (( i = 0; i < RECORDS; i++ )); do
    sector=$(printf 'sector-%02d' $(( i % 12 + 1 )))
    mkdir -p "$charts/$sector"
    file="$charts/$sector/HIP$(( 200000 + i * 211 )).chart"
    fake="STARS{$(head -c 12 /dev/urandom | od -An -tx1 | tr -d ' \n')}"
    owner=root
    size=$(( 1500 + RANDOM % 1100 ))
    [ "$size" -eq "$TARGET_SIZE" ] && size=$(( size + 1 ))

    if (( i == 637 )); then
        write_record "$file" "$TARGET_OWNER" "$TARGET_SIZE" "$FLAG"
        continue
    elif (( i % 30 == 0 )); then
        # Right size, wrong owner.
        size=$TARGET_SIZE
    elif (( i % 4 == 0 )); then
        # Right owner, wrong size.
        owner=$TARGET_OWNER
    fi
    write_record "$file" "$owner" "$size" "$fake"
done

# Fail the build if the challenge doesn't have exactly one answer.
matches=$(find "$charts" -type f -size "${TARGET_SIZE}c" -user "$TARGET_OWNER" | wc -l)
[ "$matches" -eq 1 ]
grep -q "$FLAG" "$(find "$charts" -type f -size "${TARGET_SIZE}c" -user "$TARGET_OWNER")"

chown "root:$user" "$home" "$charts" "$charts"/sector-*
chmod 750 "$home" "$charts" "$charts"/sector-*
