FROM python:3.12-slim AS base
ARG NIGHTLY=0

# Install packages needed to run your application (not build deps):
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
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
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

ADD requirements/ /requirements/
ENV VIRTUAL_ENV=/venv PATH=/venv/bin:$PATH PYTHONPATH=/code/

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
    && if [ "$NIGHTLY" = "1" ]; then \
        NIGHTLY_URL=$(curl -s https://releases.wagtail.org/nightly/latest.json | \
            grep -o 'https://[^"]*') \
        && sed -i "s|wagtail>=.*|${NIGHTLY_URL}|" /requirements/base.txt; \
    fi \
    && python3.12 -m venv ${VIRTUAL_ENV} \
    && python3.12 -m pip install -U pip \
    && python3.12 -m pip install --no-cache-dir -r /requirements/production.txt \
    && git clone -b dev --single-branch https://github.com/wagtail/wagtail-ai.git /wagtail-ai \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

FROM node:22-slim AS node

COPY --from=base /wagtail-ai /wagtail-ai
WORKDIR /wagtail-ai
RUN npm ci && npm run build

FROM base AS final

COPY --from=node /wagtail-ai/src/wagtail_ai/static /wagtail-ai/src/wagtail_ai/static
RUN python3.12 -m pip install /wagtail-ai

RUN mkdir /code/
WORKDIR /code/
ADD . /code/
ENV PORT=8000
EXPOSE 8000

# Add custom environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=bakerydemo.settings.production DJANGO_DEBUG=off

# Call collectstatic with dummy environment variables:
RUN DATABASE_URL=postgres://none REDIS_URL=none python manage.py collectstatic --noinput

# make sure static files are writable by uWSGI process
RUN mkdir -p /code/bakerydemo/media/images && mkdir -p /code/bakerydemo/media/original_images && chown -R 1000:2000 /code/bakerydemo/media

# mark the destination for images as a volume
VOLUME ["/code/bakerydemo/media/images/"]

# start uWSGI, using a wrapper script to allow us to easily add more commands to container startup:
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
CMD ["uwsgi", "/code/etc/uwsgi.ini"]
