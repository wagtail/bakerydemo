release: yes "yes" | python manage.py migrate
web: uwsgi --http :$PORT --module bakerydemo.heroku_wsgi --master --offload-threads 1
