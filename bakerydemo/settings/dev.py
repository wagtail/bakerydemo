from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

# Provide entry point to Vagrant specific settings
try:
    from .vagrant import *
except ImportError:
    pass

# Provide entry point to local specific settings
try:
    from .local import *
except ImportError:
    pass
