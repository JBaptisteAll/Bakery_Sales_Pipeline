FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY  pyproject.toml uv.lock .

RUN uv sync --locked

COPY exercices/05_docker/mock_erp/main.py .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]