.PHONY: lint format

help:
	@echo "lint - check style with black, flake8, sort python with isort, and indent html"
	@echo "format - enforce a consistent code style across the codebase and sort python files with isort"

lint:
	black --target-version py37 --check --diff .
	flake8
	isort --check-only --diff .
	curlylint --parse-only bakerydemo
	git ls-files '*.html' | xargs djhtml --check

format:
	black --target-version py37 .
	isort .
	git ls-files '*.html' | xargs djhtml -i
