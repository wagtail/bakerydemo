MANAGE = python manage.py
SOURCE = src
MAIN = src
NAME = testb
PROJECT_DIR=$(shell pwd)
WSGI_PORT=8000

run:
	$(MANAGE) runserver

run-both:
#	$(MANAGE) init_project
	npm install --prefix ./frontend
	npm run watch --prefix ./frontend & $(MANAGE) runserver && fg

seed:
	$(MANAGE) load_initial_data

vite:
	npm run watch --prefix ./frontend

docker-run:
	$(MANAGE) migrate
	$(MANAGE) load_initial_data
	$(MANAGE) runserver 0.0.0.0:$(WSGI_PORT)

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

update_index:
	"Rebuild search indexes to improve searching quality and speed."
	"https://docs.wagtail.org/en/stable/topics/search/indexing.html#the-update-index-command"
	$(MANAGE) update_index

help:
	@echo "lint - check style with black, flake8, sort python with isort, and indent html"
	@echo "format - enforce a consistent code style across the codebase and sort python files with isort"

# Local Docker
# ------------------------------------------------------------------------------
up:
	sudo docker compose up --build

down:
	sudo docker compose down
