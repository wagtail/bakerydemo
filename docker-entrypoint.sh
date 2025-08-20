#!/bin/sh
set -e

# Wait for Postgres to become available
until psql "$DATABASE_URL" -c '\q' >/dev/null 2>&1; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

# Run database migrations
/venv/bin/python manage.py migrate --noinput

# Load initial data if DJANGO_LOAD_INITIAL_DATA is set to 'on'
if [ "x$DJANGO_LOAD_INITIAL_DATA" = "xon" ]; then
  /venv/bin/python manage.py loaddata initial_data.json
fi

# Execute the container CMD
exec "$@"
