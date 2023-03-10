ARG PYTHON_TAG=3.10

# Tests
FROM python:${PYTHON_TAG} as build_test
ARG POETRY_VERSION=1.3.2

RUN pip install --no-cache-dir "poetry~=$POETRY_VERSION"
RUN useradd --create-home user
USER user

COPY --chown=user:user ./pyproject.toml /app/pyproject.toml
COPY --chown=user:user ./poetry.lock /app/poetry.lock

WORKDIR /app

RUN poetry install --no-cache --no-interaction

COPY --chown=user:user . /app

RUN poetry export -f requirements.txt > requirements.txt

# Project stage
FROM python:${PYTHON_TAG}
ENV PYTHONUNBUFFERED=1\
    PYTHONDONTWRITEBYTECODE=1

RUN useradd --create-home user
WORKDIR /app

COPY --from=build_test --chown=user:user /app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=user:user ./gitlab_bot /app/gitlab_bot
RUN chown user:user -R /app/

USER user
ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "--bind", "0.0.0.0:8080", "gitlab_bot:app"]
