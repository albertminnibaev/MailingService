FROM python:3.12

RUN curl -sSL https://install.python-poetry.org | python -
WORKDIR /app

ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH="/app"

COPY pyproject.toml poetry.lock ./

RUN python -m pip install --no-cache-dir poetry==0.1.0 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . .
