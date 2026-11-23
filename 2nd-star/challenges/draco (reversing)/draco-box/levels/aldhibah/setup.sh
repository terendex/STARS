#!/bin/bash
# Aldhibah (Hard): the program hibernates for a thousand years, then only prints
# the flag for a rider of rank 7 (root). Players skip the sleep, then fake the
# rank, in gdb with `return`.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=aldhibah
FLAG='STARS{4ldh1b4h_r4nk_s3v3n_r1d3r}'
KEY=0x71

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -Wl,-z,lazy -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" \
    -o "$home/aldhibah" aldhibah.c

# Fail the build if strings shows the flag, if skipping only the sleep is
# enough, or if the gdb steps from the answer sheet don't work. The build runs as
# root, and root really is rank 7, so gdb runs as the player.
if strings "$home/aldhibah" | grep -qF STARS; then echo "strings finds aldhibah's flag" >&2; exit 1; fi
out=$(runuser -u "$user" -- gdb -q -batch -ex 'break hibernate' -ex run -ex return -ex continue "$home/aldhibah" 2>&1 || true)
grep -qF "only speaks to riders of rank 7" <<<"$out"
if grep -qF STARS <<<"$out"; then echo "aldhibah gives its flag without the rank" >&2; exit 1; fi
runuser -u "$user" -- gdb -q -batch -ex 'break hibernate' -ex 'break rider_rank' -ex run -ex return -ex continue -ex 'return 7' -ex continue "$home/aldhibah" 2>&1 | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/aldhibah"
