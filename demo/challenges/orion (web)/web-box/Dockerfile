# The demo's Orion stars. Same setup as the real web-box, without Alnitak's database.
FROM python:3.12-slim

RUN pip install --no-cache-dir flask==3.1.2 gunicorn==23.0.0
RUN useradd -M -s /usr/sbin/nologin web

WORKDIR /app
COPY *.py ./

USER web
EXPOSE 8000
# The service's command picks the app, for example saiph:app
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "1", "--worker-tmp-dir", "/tmp"]
