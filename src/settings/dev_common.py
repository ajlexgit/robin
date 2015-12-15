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

# Вывод ошибок в консоль
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}
