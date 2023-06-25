FROM python:3.10-bullseye

RUN apt-get install libbz2-dev

RUN pip install poetry

COPY tcc/pyproject.toml tcc/poetry.lock /app/tcc/

WORKDIR /app/tcc/

RUN poetry install

WORKDIR /app

COPY . .