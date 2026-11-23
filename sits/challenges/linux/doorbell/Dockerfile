# Knock Knock's doorbell: sends message.txt to anyone who connects to port
# 5287. It's on the challenges' private network only, so players reach it from
# the Linux box.
FROM debian:13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -M -s /usr/sbin/nologin doorbell

COPY message.txt /doorbell/message.txt
RUN chmod 444 /doorbell/message.txt

USER doorbell
EXPOSE 5287
CMD ["socat", "TCP-LISTEN:5287,reuseaddr,fork,max-children=32", "OPEN:/doorbell/message.txt,rdonly"]
