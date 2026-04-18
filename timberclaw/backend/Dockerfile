# TimberClaw Django API — minimal image for docker-compose (M0-01).
FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY pytest.ini .
COPY manage.py .
COPY tc_project ./tc_project
COPY accounts ./accounts
COPY tests ./tests

EXPOSE 8000

# Dev-friendly server for scaffold; swap to gunicorn in M0-05+.
CMD ["sh", "-c", "python manage.py migrate --noinput && exec python manage.py runserver 0.0.0.0:8000"]
