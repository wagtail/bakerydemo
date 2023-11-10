.PHONY: lint format

help:
	@echo "lint - check style with black, ruff, sort python with ruff, indent html, and lint frontend css/js"
	@echo "format - enforce a consistent code style across the codebase, sort python files with ruff and fix frontend css/js"

lint-server:
	black --target-version py38 --check --diff .
	ruff check .
	curlylint --parse-only bakerydemo
	git ls-files '*.html' | xargs djhtml --check

lint-client:
	npm run lint:css --silent
	npm run lint:js --silent
	npm run lint:format --silent

lint: lint-server lint-client

format-server:
	black --target-version py38 .
	ruff check . --fix
	git ls-files '*.html' | xargs djhtml -i

format-client:
	npm run format
	npm run fix:js

format: format-server format-client
