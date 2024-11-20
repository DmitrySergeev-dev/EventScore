FROM python:3.10-slim as python-base

# Set environment variables
ENV TZ=Europe/Moscow \
    # python:
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # poetry:
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    # Для запуска WSGI сервера
    PATH="$POETRY_HOME/bin:$PATH"


WORKDIR /app

# Устанавливаем менеджер для управления зависимостями
RUN pip install poetry

# Устанавливаем зависимости
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install

# Копируем остальной код приложения
COPY .env ./
COPY scripts ./scripts
COPY alembic.ini ./
COPY migrations ./migrations
COPY src ./src

# Указываем команду для запуска приложения
CMD ["python", "src/entrypoints/main.py"]
#CMD ["uvicorn", "src.entrypoints.app:app", "--host", "0.0.0.0", "--port", "8005"]






