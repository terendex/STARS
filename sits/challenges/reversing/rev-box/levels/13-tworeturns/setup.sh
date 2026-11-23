#!/bin/bash
# Two Returns (Hard): the program waits a thousand years, then only prints the
# flag for a tier 3 VIP (root). Players skip the wait, then fake the tier, in
# gdb with `return`.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=tworeturns
FLAG='FLAG{tw0_r3turns_g0t_m3_1n}'
KEY=0x5c

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

scrambled() {
    python3 -c 'import sys; print("{" + ",".join(hex(ord(c) ^ int(sys.argv[2], 0)) for c in sys.argv[1]) + "}")' "$1" "$KEY"
}

gcc -O0 -g -fno-builtin -no-pie -Wl,-z,lazy -DKEY="$KEY" -DFLAG_BYTES="$(scrambled "$FLAG")" -o "$home/vip" vip.c

# The build runs as root, and root really is tier 3, so gdb runs as the player.
if strings "$home/vip" | grep -qF 'FLAG{'; then echo "strings finds the flag" >&2; exit 1; fi
out=$(runuser -u "$user" -- gdb -q -batch -ex 'break queue_up' -ex run -ex return -ex continue "$home/vip" 2>&1 || true)
grep -qF "Only tier 3 VIPs get in tonight" <<<"$out"
if grep -qF 'FLAG{' <<<"$out"; then echo "skipping only the wait is enough" >&2; exit 1; fi
runuser -u "$user" -- gdb -q -batch -ex 'break queue_up' -ex 'break vip_tier' -ex run -ex return -ex continue -ex 'return 3' -ex continue "$home/vip" 2>&1 | grep -qF "$FLAG"

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/vip"
