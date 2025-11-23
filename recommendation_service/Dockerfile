FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]