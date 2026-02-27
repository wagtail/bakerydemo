# Contributing to Bakerydemo

Thank you for contributing to **Wagtail Bakerydemo**! This project demonstrates common Wagtail CMS features and is used as a learning resource.  

## Getting Started

### 1. Clone & install
```bash
git clone https://github.com/wagtail/bakerydemo.git
cd bakerydemo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt

2. Create local config
cp bakerydemo/settings/local.py.example bakerydemo/settings/local.py
cp .env.example .env

3. Migrate & load data
./manage.py migrate
./manage.py load_initial_data
./manage.py runserver

Development Tasks
Lint & format
ruff check .
ruff format .

Run tests
pytest

Update fixture data
./manage.py dumpdata --natural-foreign --indent 2 \
  -e auth.permission -e contenttypes -e wagtailimages.rendition \
  -e wagtailsearch.indexentry -e sessions \
  > bakerydemo/base/fixtures/bakerydemo.json

npx prettier --write bakerydemo/base/fixtures/bakerydemo.json

Pull Request Guidelines

Keep PRs focused and well-explained.

Ensure formatting and lint checks pass.

Update documentation when needed.

Link related issues.

Thank you for helping improve Bakerydemo!

```md
# Contributing to Bakerydemo

We appreciate your interest in contributing to **Wagtail Bakerydemo**.  
This repository serves as an educational reference implementation for Wagtail CMS and is maintained to support developers exploring Wagtail’s features and best practices.

This document outlines the recommended development setup, coding standards, and contribution workflow.

---

## 1. Development Environment Setup

### Clone the repository
```bash
git clone https://github.com/wagtail/bakerydemo.git
cd bakerydemo

Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

Install development dependencies
pip install -r requirements/development.txt

Create local configuration files
cp bakerydemo/settings/local.py.example bakerydemo/settings/local.py
cp .env.example .env

Apply migrations and load initial data
./manage.py migrate
./manage.py load_initial_data
./manage.py runserver


Access the admin interface at /admin/ using:

Username: admin
Password: changeme

2. Development Standards
Code formatting and linting

This project uses Ruff for both linting and code formatting.

ruff check .
ruff format .

Running tests
pytest

Updating demo fixtures

If modifying content included in the demo data, regenerate the fixture:

./manage.py dumpdata --natural-foreign --indent 2 \
  -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission \
  -e wagtailimages.rendition -e wagtailsearch.indexentry -e sessions \
  > bakerydemo/base/fixtures/bakerydemo.json

npx prettier --write bakerydemo/base/fixtures/bakerydemo.json

3. Contribution Workflow
To maintain quality and clarity across contributions:
Open an issue before large changes when possible.
Keep pull requests focused on a single change or topic.
Ensure all tests and linters pass before submitting your PR.
Add or update documentation if you introduce new behavior.
Reference related issues in your pull request description.
Be open to feedback during code review.

4. Further Resources
Wagtail documentation: https://docs.wagtail.org/en/stable/
Wagtail contributor guide: https://docs.wagtail.org/en/stable/contributing/

Thank you for contributing to Bakerydemo. Your work directly supports the Wagtail community by improving its most widely used learning resource.
