from .base import *  # noqa

DEBUG = False

# Make sure Django can detect a secure connection properly on Heroku:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Redirect all requests to HTTPS
SECURE_SSL_REDIRECT = True
