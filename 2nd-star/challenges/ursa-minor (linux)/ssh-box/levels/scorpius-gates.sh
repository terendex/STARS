#!/bin/bash
# Windows doesn't ship with nc, so these accounts let Scorpius players connect
# with SSH instead. Logging in goes straight to the star's program, with no shell.
# Antares isn't here because it needs raw bytes, which a terminal would mangle.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

for star in shaula sargas lesath dschubba acrab; do
    useradd -M -d / -s /bin/bash -G players "$star"
    echo "$star:scorpius" | chpasswd
    cat >> /etc/ssh/sshd_config <<EOF

Match User $star
    # socat rather than nc, because nc would leave the session hanging after
    # the program finishes.
    ForceCommand socat - TCP:$star:9001
EOF
done
