FROM debian:13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server less file netcat-openbsd socat \
    && rm -rf /var/lib/apt/lists/*

COPY sshd_config /etc/ssh/sshd_config
COPY banner.txt /etc/ssh/banner.txt
COPY levels/ /build/levels/
# The server's own keys, if host-keys/ holds the ones from the last build (see
# README, "Keeping the SSH keys"), so players who connected before don't see
# "REMOTE HOST IDENTIFICATION HAS CHANGED". The wildcard lets the folder be
# missing, and then ssh-keygen makes new keys. banner.txt is only there because
# COPY needs at least one file that exists.
COPY banner.txt host-key[s] /build/host-keys/

# Each levels/*.sh creates one player account. The sed keeps scripts working
# if they were saved with Windows line endings.
RUN sed -i 's/\r$//' /etc/ssh/sshd_config /etc/ssh/banner.txt /build/levels/*.sh \
    && groupadd players \
    && for level in /build/levels/*.sh; do bash "$level"; done \
    && if ls /build/host-keys/ssh_host_*_key >/dev/null 2>&1; then \
           cp /build/host-keys/ssh_host_* /etc/ssh/ \
           && chmod 600 /etc/ssh/ssh_host_*_key && chmod 644 /etc/ssh/ssh_host_*_key.pub; \
       fi \
    && rm -rf /build \
    && ssh-keygen -A

EXPOSE 22
CMD ["/bin/sh", "-c", "mkdir -p /run/sshd && exec /usr/sbin/sshd -D -e"]
