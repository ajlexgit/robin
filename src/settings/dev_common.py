from settings.common import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = (
    'localhost',
    'local.ru',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project',
        'USER': 'project',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
}


INSTALLED_APPS = (
    'devserver',
) + INSTALLED_APPS


MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'devserver.middleware.DevServerMiddleware',
)

PIPELINE_ENABLED = True

# Devserver
DEVSERVER_SQL_MIN_DURATION = 100

# Smart Cache-Control
SCC_PREVENT_CACHING = True
