#!/bin/sh
set -e

until psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "$1" = '/venv/bin/uwsgi' ]; then
    /venv/bin/python manage.py migrate --noinput
fi

if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
	/venv/bin/python manage.py load_initial_data
fi

exec "$@"
