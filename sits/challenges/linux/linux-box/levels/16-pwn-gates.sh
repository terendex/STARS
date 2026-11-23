#!/bin/bash
# Windows doesn't ship with nc, so these accounts let Pwn players connect with
# SSH instead. Logging in goes straight to the program, with no shell.
# Return to Sender (antares) isn't here because it needs raw bytes, which a
# terminal would mangle; players use nc from any Linux account for that one.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

# account:program
for gate in menu:shaula shop:sargas nametag:lesath vault:fang greeter:larawag exactfit:dschubba echoecho:acrab; do
    account=${gate%%:*}
    program=${gate##*:}
    useradd -M -d / -s /bin/bash -G players "$account"
    echo "$account:pwnit" | chpasswd
    cat >> /etc/ssh/sshd_config <<CONF

Match User $account
    # socat rather than nc, because nc would leave the session hanging after
    # the program finishes.
    ForceCommand socat - TCP:$program:9001
CONF
done
