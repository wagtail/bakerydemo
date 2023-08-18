MANAGE = python manage.py
SOURCE = src
MAIN = src
NAME = testb
PROJECT_DIR=$(shell pwd)
WSGI_PORT=8000

run:
	$(MANAGE) runserver

install:
	poetry install

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

update_index:
	$(MANAGE) update_index

help:
	@echo "lint - check style with black, flake8, sort python with isort, and indent html"
	@echo "format - enforce a consistent code style across the codebase and sort python files with isort"
