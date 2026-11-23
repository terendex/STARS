#!/bin/bash
# Exact Size (Medium): one real parcel among 1,000 decoys, spread over 10 shelves.
# Every decoy carries a fake flag, so a plain grep isn't enough: players filter
# by size and owner with find.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=exactsize
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:measuring" | chpasswd
useradd -M -s /usr/sbin/nologin courier

home="/home/$user"
store="$home/warehouse"
mkdir -p "$store"

FLAG='FLAG{s1z3d_4nd_s1gn3d_f0r}'
TARGET_SIZE=1234
TARGET_OWNER=courier
RANDOM=1234

write_parcel() {
    local file=$1 owner=$2 size=$3 flag=$4
    local header
    header=$(printf 'parcel %s\nflag: %s\ncontents: ' "$(basename "$file" .box)" "$flag")
    local pad=$(( size - ${#header} ))
    {
        printf '%s' "$header"
        head -c "$pad" /dev/urandom | base64 -w0 | cut -c1-"$pad" | tr -d '\n'
    } > "$file"
    chown "$owner:$user" "$file"
    chmod 640 "$file"
}

for (( i = 0; i < 1000; i++ )); do
    shelf=$(printf 'shelf-%02d' $(( i % 10 + 1 )))
    mkdir -p "$store/$shelf"
    file="$store/$shelf/parcel-$(( 40000 + i * 37 )).box"
    fake="FLAG{$(head -c 12 /dev/urandom | od -An -tx1 | tr -d ' \n')}"
    owner=root
    size=$(( 900 + RANDOM % 700 ))
    [ "$size" -eq "$TARGET_SIZE" ] && size=$(( size + 1 ))

    if (( i == 444 )); then
        write_parcel "$file" "$TARGET_OWNER" "$TARGET_SIZE" "$FLAG"
        continue
    elif (( i % 25 == 0 )); then
        size=$TARGET_SIZE        # right size, wrong owner
    elif (( i % 5 == 0 )); then
        owner=$TARGET_OWNER      # right owner, wrong size
    fi
    write_parcel "$file" "$owner" "$size" "$fake"
done

# Fail the build unless size and owner together find exactly the flag, and
# neither does alone.
[ "$(find "$store" -type f -size "${TARGET_SIZE}c" -user "$TARGET_OWNER" | wc -l)" -eq 1 ]
grep -q "$FLAG" "$(find "$store" -type f -size "${TARGET_SIZE}c" -user "$TARGET_OWNER")"
[ "$(find "$store" -type f -size "${TARGET_SIZE}c" | wc -l)" -gt 1 ]
[ "$(find "$store" -type f -user "$TARGET_OWNER" | wc -l)" -gt 1 ]

chown "root:$user" "$home" "$store" "$store"/shelf-*
chmod 750 "$home" "$store" "$store"/shelf-*
