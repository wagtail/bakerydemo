MANAGE = python manage.py
SOURCE = src
MAIN = src
NAME = testb
PROJECT_DIR=$(shell pwd)
WSGI_PORT=8000

run:
#	$(MANAGE) init_project
	npm install --prefix ./frontend
	npm run watch --prefix ./frontend & $(MANAGE) runserver && fg

vite:
	npm run watch --prefix ./frontend

docker-run:
	$(MANAGE) migrate
	$(MANAGE) load_initial_data
	$(MANAGE) runserver 0.0.0.0:$(WSGI_PORT)

seed:
	$(MANAGE) load_initial_data

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

# Local Docker
# ------------------------------------------------------------------------------
up:
	sudo docker compose up --build

down:
	sudo docker compose down
