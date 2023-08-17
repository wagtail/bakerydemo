MANAGE = python manage.py
SOURCE = src
MAIN = src
NAME = testb


PROJECT_DIR=$(shell pwd)
WSGI_PORT=8000


run:
	$(MANAGE) runserver


migrations:
	$(MANAGE) migrations


migrate:
	$(MANAGE) migrate
