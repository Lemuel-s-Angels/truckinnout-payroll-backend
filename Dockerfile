FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    libpq \
    musl-dev \
    postgresql-dev \
    python3-dev

COPY requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn

COPY . /app/

RUN adduser -D appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app/staticfiles /app/media

USER appuser
