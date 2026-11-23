# Shared by every Scorpius star. Build with --build-arg STAR=<star>.
FROM debian:13-slim AS build
ARG STAR
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY ${STAR}/dist/${STAR}.c /src/${STAR}.c
# Protections are off on purpose: this is the challenge.
RUN gcc -O0 -static -no-pie -fno-pie -fno-stack-protector -Wno-unused-result -Wno-format-security \
    -o /src/${STAR} /src/${STAR}.c

# Exports a compiled player download, for example:
#   docker build --target dist --build-arg STAR=antares --output antares/dist .
FROM scratch AS dist
ARG STAR
COPY --from=build /src/${STAR} /${STAR}

FROM debian:13-slim AS service
ARG STAR
RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -M -s /usr/sbin/nologin ctf
COPY --from=build /src/${STAR} /chal/challenge
COPY ${STAR}/src/flag.txt /flag.txt
RUN chown root:ctf /flag.txt && chmod 440 /flag.txt

USER ctf
EXPOSE 9001
CMD ["socat", "TCP-LISTEN:9001,reuseaddr,fork,max-children=32", "EXEC:timeout 300 /chal/challenge,stderr"]
