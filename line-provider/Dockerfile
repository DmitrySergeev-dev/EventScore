FROM python:3.10-slim

ENV POETRY_VERSION=1.6.0
ENV PATH="/root/.local/bin:$PATH"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /var/www/line-provider
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN poetry install --no-root --no-dev

COPY . ./

CMD ["fastapi", "run", "src/app.py", "--port", "8005"]

#CMD ["poetry", "run", "python", "your_script.py"]