# The 2nd demo's Orion star. Same setup as the first demo's web-box.
FROM python:3.12-slim

RUN pip install --no-cache-dir flask==3.1.2 gunicorn==23.0.0
RUN useradd -M -s /usr/sbin/nologin web

WORKDIR /app
COPY *.py ./

USER web
EXPOSE 8000
# The service's command picks the app, for example flame_nebula:app
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "1", "--worker-tmp-dir", "/tmp"]
