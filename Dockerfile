# Base image
FROM python:3.12-slim
ARG NIGHTLY=0

# Install runtime dependencies
RUN set -ex \
    && RUN_DEPS=" \
        libexpat1 \
        libjpeg62-turbo \
        libpcre2-posix3 \
        libpq5 \
        shared-mime-info \
        postgresql-client \
        procps \
        zlib1g \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*
ADD requirements/ /requirements/

# Set environment variables for Python
ENV VIRTUAL_ENV=/venv
ENV PATH=/venv/bin:$PATH
ENV PYTHONPATH=/code/

# Install build dependencies, then Python packages
RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        curl \
        git \
        libexpat1-dev \
        libjpeg62-turbo-dev \
        libpcre2-dev \
        libpq-dev \
        zlib1g-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && python3.12 -m venv ${VIRTUAL_ENV} \
    && python3.12 -m pip install -U pip \
    && python3.12 -m pip install --no-cache-dir gunicorn \
    && python3.12 -m pip install --no-cache-dir -r /requirements/production.txt \
    && apt-get purge -y --auto-remove $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# Set port and environment variables
ENV PORT=8000
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=bakerydemo.settings.production
ENV DJANGO_DEBUG=off

# Collect static files
RUN DATABASE_URL=postgres://none REDIS_URL=none python manage.py collectstatic --noinput

# Make sure media directories exist
RUN mkdir -p /code/bakerydemo/media/images \
    && mkdir -p /code/bakerydemo/media/original_images \
    && chown -R 1000:2000 /code/bakerydemo/media

# Mark media/images as a volume
VOLUME ["/code/bakerydemo/media/images/"]

# Start Gunicorn instead of uWSGI
CMD ["gunicorn", "bakerydemo.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--log-level", "debug"]
