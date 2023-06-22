# https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/python3.11-slim.dockerfile
FROM python:3.11-slim-bookworm

WORKDIR /

# Install Poetry
RUN pip --disable-pip-version-check --no-cache-dir install poetry
RUN poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /
RUN poetry install --no-root --without=dev --no-cache

COPY ./gunicorn_conf.py /gunicorn_conf.py
COPY ./server/start.sh /start.sh
COPY ./server/prestart.sh /prestart.sh
RUN set -eux \
    chmod +x /start.sh; \
    chmod +x /prestart.sh; 

COPY ./app /app

WORKDIR /app

ENV PYTHONPATH=/app
ENV PRE_START_PATH=/prestart.sh
ENV PORT=8001

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
