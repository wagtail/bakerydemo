from whitenoise.django import DjangoWhiteNoise

from .wsgi import application as _application


application = DjangoWhiteNoise(_application)
