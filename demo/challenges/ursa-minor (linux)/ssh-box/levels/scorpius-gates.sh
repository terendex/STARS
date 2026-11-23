#!/bin/bash
# SSH logins for the demo's Scorpius stars, for players without nc. Logging in
# goes straight to the star's program, with no shell. See the real SSH box's
# scorpius-gates.sh.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

for star in fang larawag; do
    useradd -M -d / -s /bin/bash -G players "$star"
    echo "$star:scorpius" | chpasswd
    cat >> /etc/ssh/sshd_config <<CONF

Match User $star
    ForceCommand socat - TCP:$star:9001
CONF
done
