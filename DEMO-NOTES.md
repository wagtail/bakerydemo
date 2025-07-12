# Wagtail Unveil Demo Notes

The files in this commit are the chnages I made to use the package in the bakery demo project.

Currently installed via `pip install git+`

## Changes made

- Added wagtail-unveil to `requirements/development.txt`
- Added `wagtail_unveil.api_urls` to the bakerydemo `urls.py` (optional for JSON views)
- Added local.py to for settings with the following content:

```python
from .base import INSTALLED_APPS

INSTALLED_APPS += [
    'wagtail_unveil',
]

# List of models to include in the Generic Models report
# These should be models managed by ModelViewSet or other generic views
WAGTAIL_UNVEIL_GENERIC_MODELS = ['breads.Country']

# List of Wagtail ModelAdmin models to include in the Wagtail ModelAdmin report
# These should be models registered with Wagtail's ModelAdmin
# WAGTAIL_UNVEIL_WAGTAIL_MODELADMIN_MODELS = ['core.ExampleWagtailModeladminModel']

# Maximum number of instances to include per model in unveil reports
# WAGTAIL_UNVEIL_MAX_INSTANCES = 1 # optional, the default is

# Position the Unveil reports menu item in the Wagtail admin menu
# WAGTAIL_UNVEIL_MENU_ORDER = 1 # optional, the default is 1

# Base URL for generating URLs in reports
# This should be the base URL of your Wagtail site, e.g. "http://localhost:8000"
# WAGTAIL_UNVEIL_BASE_URL = "http://localhost:8000"

# Token for accessing the JSON API endpoints
# This is used for authentication when accessing the API endpoints.
# Admin users can access the API without a token, but for external access, you should set this.
WAGTAIL_UNVEIL_JSON_TOKEN = "1234"
```

Followed the bakery demo instructions to set up the project and run the server, including loading the initial data.