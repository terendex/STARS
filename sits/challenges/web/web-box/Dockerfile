# Every SITS web challenge runs from this one image; the service's command picks
# the app, for example view_source:app.
FROM python:3.12-slim

RUN pip install --no-cache-dir flask==3.1.2 gunicorn==23.0.0
RUN useradd -M -s /usr/sbin/nologin web

WORKDIR /app
COPY *.py ./

# Sign In Anyway's and The Union's databases are built once and are read-only
# from then on.
RUN python init_dbs.py && rm init_dbs.py

USER web
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "1", "--worker-tmp-dir", "/tmp"]
