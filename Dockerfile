FROM python:3.11-slim
LABEL maintainer="DimitarITZankov"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 4000

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        python3-dev \
        build-essential \
        postgresql-client \
        && python -m venv /py \
        && /py/bin/pip install --upgrade pip \
        && /py/bin/pip install -r /tmp/requirements.txt \
        && rm -rf /var/lib/apt/lists/* /tmp/requirements.txt

RUN adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"
USER django-user