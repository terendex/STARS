# 11 UMi's beacon: sends a message to anyone who connects to its port. It sits
# on the challenges' private network with no published port, so players can
# only reach it from the SSH box (see ssh-box/levels/umi11.sh).
FROM debian:13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -M -s /usr/sbin/nologin beacon

COPY message.txt /beacon/message.txt
RUN chmod 444 /beacon/message.txt

USER beacon
EXPOSE 4731
CMD ["socat", "TCP-LISTEN:4731,reuseaddr,fork,max-children=32", "OPEN:/beacon/message.txt,rdonly"]
