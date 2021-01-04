FROM python:3.8-slim-buster

ENV VIRTUAL_ENV=/opt/venv
# make the venv, and append to the PATH
RUN python -m venv $VIRTUAL_ENV && pip install poetry
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install torch
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install
RUN apt-get update \
    && apt-get install -y wget \
    && apt-get install unzip \
    && wget "https://www.dropbox.com/s/gtwnyp9n49lqs7t/saved-models.zip?dl=0" \
    && unzip saved-models.zip?dl=0\
    && rm -rf /var/lib/apt/lists/*

COPY . .