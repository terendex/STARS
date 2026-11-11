FROM python:3.12-slim

RUN pip install --no-cache-dir flask==3.1.2 gunicorn==23.0.0
RUN useradd -M -s /usr/sbin/nologin rigel

WORKDIR /app
COPY app.py init_db.py ./
COPY templates/ templates/

# The database is built once and is read-only from then on.
RUN python init_db.py && rm init_db.py

USER rigel
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "--worker-tmp-dir", "/tmp", "app:app"]
