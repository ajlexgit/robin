from django.conf import settings

SECRET = settings.SPHINX_SECRET
HOST = getattr(settings, 'SPHINX_HOST', 'localhost')
PORT = getattr(settings, 'SPHINX_PORT', '9312')
