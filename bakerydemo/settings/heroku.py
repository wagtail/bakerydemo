import dj_database_url

from .base import *


DEBUG = True

# Accept all hostnames, since we don't know in advance which hostname will be used for any given Heroku instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*', 'wagtailbakerydemo.herokuapp.com']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

DATABASES = {'default': dj_database_url.config(default='postgres://postgres@localhost:5432/wagtaildemo')}


try:
    from .local import *
except ImportError:
    pass
