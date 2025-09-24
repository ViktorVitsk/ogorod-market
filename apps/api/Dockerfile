FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем только зависимости (без проекта)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копируем исходный код (кроме того что в .dockerignore)
COPY . .

# Теперь устанавливаем проект
RUN poetry install --no-interaction --no-ansi

# Создаем недостающие папки
RUN mkdir -p alembic/versions

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]