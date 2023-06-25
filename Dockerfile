FROM python:3.10-bullseye

RUN apt-get install libbz2-dev
WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry install

COPY . .