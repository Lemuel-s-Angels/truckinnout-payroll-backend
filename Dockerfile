FROM python:3.12-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

ENV UV_NO_DEV=1
WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN uv sync --frozen
