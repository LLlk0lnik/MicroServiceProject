FROM python:3.12-slim AS builder

RUN pip install poetry==2.4.1

ENV POETRY_NO_INTERACTION=1\
    POETRY_VIRTUALENVS_IN_PROJECT=1\
    POETRY_VIRTUALENVS_CREATE=1\
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

COPY README.md /app/README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root --only main

FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src/ /app/src

WORKDIR /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
