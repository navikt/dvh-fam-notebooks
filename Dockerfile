FROM navikt/python:3.10
LABEL org.opencontainers.image.source "https://github.com/navikt/dvh-fam-notebooks"

USER root

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY src ./

USER apprunner
