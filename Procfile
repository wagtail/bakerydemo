release: yes "yes" | python manage.py migrate
web: uwsgi --http :$PORT --module bakerydemo.wsgi --master --offload-threads 1
