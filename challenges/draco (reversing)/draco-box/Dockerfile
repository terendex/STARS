# Draco's SSH box: one account per star, each holding that star's program, with
# the reversing tools already installed, so players don't need to install any.
# The demo builds this same Dockerfile with its own levels.
FROM debian:13-slim

# The players' tools: strings and objdump (from binutils), ltrace, gdb and python3.
# Docker doesn't let gdb turn off address randomization, so gdb is told not to
# try. Otherwise it prints a scary warning every time a beginner runs a program.
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server less file nano xxd binutils ltrace gdb python3 \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'set disable-randomization off' >> /etc/gdb/gdbinit

COPY sshd_config /etc/ssh/sshd_config
COPY banner.txt /etc/ssh/banner.txt
COPY levels/ /build/levels/

# Each levels/<star>/setup.sh creates one player account and builds that star's
# program into its home folder, then checks the level can be solved. gcc is only
# needed for the build, so it's removed in the same step. The sed keeps the
# files working if they were saved with Windows line endings.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && find /etc/ssh/sshd_config /etc/ssh/banner.txt /build/levels -type f -exec sed -i 's/\r$//' {} + \
    && groupadd players \
    && for setup in /build/levels/*/setup.sh; do (cd "$(dirname "$setup")" && bash setup.sh); done \
    && apt-get purge -y --auto-remove gcc libc6-dev \
    && rm -rf /build /var/lib/apt/lists/* \
    && ssh-keygen -A

EXPOSE 22
CMD ["/bin/sh", "-c", "mkdir -p /run/sshd && exec /usr/sbin/sshd -D -e"]
