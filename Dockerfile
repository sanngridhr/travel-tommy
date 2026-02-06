# --- BASE IMAGE --- #
FROM python:3.13-slim AS runtime

# --- ENV --- #
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DB_PATH=/root/db.sqlite3

# --- INSTALL SYSTEM DEPENDENCIES --- #
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - --version 2.2.1
ENV PATH="/root/.local/bin:$PATH"

# --- SET WORK DIRECTORY --- #
WORKDIR /app

# --- INSTALL PYTHON DEPENDENCIES --- #
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# --- COPY CODE --- #
COPY src ./src

# --- RUN --- #
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]