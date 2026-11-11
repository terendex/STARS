FROM debian:13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server less file netcat-openbsd socat \
    && rm -rf /var/lib/apt/lists/*

COPY sshd_config /etc/ssh/sshd_config
COPY banner.txt /etc/ssh/banner.txt
COPY levels/ /build/levels/

# Each levels/*.sh creates one player account. The sed keeps scripts working
# if they were saved with Windows line endings.
RUN sed -i 's/\r$//' /etc/ssh/sshd_config /etc/ssh/banner.txt /build/levels/*.sh \
    && groupadd players \
    && for level in /build/levels/*.sh; do bash "$level"; done \
    && rm -rf /build \
    && ssh-keygen -A

EXPOSE 22
CMD ["/bin/sh", "-c", "mkdir -p /run/sshd && exec /usr/sbin/sshd -D -e"]
