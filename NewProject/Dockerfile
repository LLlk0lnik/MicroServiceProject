FROM python:3.14
WORKDIR /app
RUN pip install --no-cache-dir poetry==2.4.1
ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main
COPY src/ /app/src
COPY README.md /app/README.md
RUN poetry install --only-root
EXPOSE 8000
CMD ["uvicorn", "newproject.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
