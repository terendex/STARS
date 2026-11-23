# SITS's Reversing box: one account per challenge, each holding its program, with
# the reversing tools already installed, so players don't need to install any.
# (Built the same way as the STARS Draco box.)
FROM debian:13-slim

# The players' tools: strings and objdump (from binutils), ltrace, gdb and python3.
# Two changes keep gdb's output short for beginners. Docker doesn't let gdb turn
# off address randomization, so gdb is told not to try, or it prints a scary
# warning on every run. And `gdb` means `gdb -q`, which skips the 14-line
# license banner. Login shells read /etc/bash.bashrc, so the alias applies there.
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server less file nano xxd binutils ltrace gdb python3 \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'set disable-randomization off' >> /etc/gdb/gdbinit \
    && echo "alias gdb='gdb -q'" >> /etc/bash.bashrc

COPY sshd_config /etc/ssh/sshd_config
COPY banner.txt /etc/ssh/banner.txt
COPY levels/ /build/levels/
# The server's own keys, if host-keys/ holds the ones from the last build (see
# README, "Keeping the SSH keys"), so players who connected before don't see
# "REMOTE HOST IDENTIFICATION HAS CHANGED". The wildcard lets the folder be
# missing, and then ssh-keygen makes new keys. banner.txt is only there because
# COPY needs at least one file that exists.
COPY banner.txt host-key[s] /build/host-keys/

# Each levels/<name>/setup.sh creates one player account and builds that
# challenge's program into its home folder, then checks it can be solved. gcc is only
# needed for the build, so it's removed in the same step. The sed keeps the
# files working if they were saved with Windows line endings.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && find /etc/ssh/sshd_config /etc/ssh/banner.txt /build/levels -type f -exec sed -i 's/\r$//' {} + \
    && groupadd players \
    && for setup in /build/levels/*/setup.sh; do (cd "$(dirname "$setup")" && bash setup.sh) || { echo "LEVEL FAILED: $setup" >&2; exit 1; }; done \
    && apt-get purge -y --auto-remove gcc libc6-dev \
    && if ls /build/host-keys/ssh_host_*_key >/dev/null 2>&1; then \
           cp /build/host-keys/ssh_host_* /etc/ssh/ \
           && chmod 600 /etc/ssh/ssh_host_*_key && chmod 644 /etc/ssh/ssh_host_*_key.pub; \
       fi \
    && rm -rf /build /var/lib/apt/lists/* \
    && ssh-keygen -A

EXPOSE 22
CMD ["/bin/sh", "-c", "mkdir -p /run/sshd && exec /usr/sbin/sshd -D -e"]
