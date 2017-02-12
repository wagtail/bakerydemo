release: pip install -r requirements_heroku.txt
release: yes "yes" | python manage.py migrate
web: gunicorn bakerydemo.heroku_wsgi --log-file -
