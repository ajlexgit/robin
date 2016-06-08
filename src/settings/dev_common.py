from settings.common import *

DOMAIN = '.local.com'

ALLOWED_HOSTS = (
    DOMAIN,
    '127.0.0.1',
    'localhost',
)

SESSION_COOKIE_DOMAIN = DOMAIN
CSRF_COOKIE_DOMAIN = DOMAIN

DEBUG = True

DATABASES.update({
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project',
        'USER': 'project',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
})

# Отключение компрессии SASS (иначе теряется наглядность кода)
PIPELINE['SASS_ARGUMENTS'] = '-t nested'

STATICFILES_FINDERS += (
    'libs.pipeline.debug_finder.PipelineFinder',
)

# Отключение кэширования шаблонов
TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


INSTALLED_APPS = (
    'devserver',
) + INSTALLED_APPS


MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'devserver.middleware.DevServerMiddleware',
)

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
        'sql': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}
