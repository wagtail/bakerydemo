from .base import *  # noqa: F403, F401

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

ALLOWED_HOSTS = '*'
