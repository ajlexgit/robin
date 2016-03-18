from settings.common import *

DOMAIN = '.dev.direktweb.ru'
VZ_DIRECTORY = 'project.dev.direktweb.ru'

# Имя хоста (имя виртуальной машины - master, staging и т.д.), должно быть настроено на виртуалке
# Метка %HOSTNAME% при развёртывании заменяется на настоящее имя виртуалки
HOSTNAME = '%HOSTNAME%'

SESSION_COOKIE_DOMAIN = DOMAIN
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

CSRF_COOKIE_DOMAIN = DOMAIN

# Метка %SECRET_KEY% при развёртывании заменяется на нужный секретный ключ
SECRET_KEY = '%SECRET_KEY%'

ALLOWED_HOSTS = (
    DOMAIN,
)

# настройки статики
STATIC_ROOT = '/home/webapp/%s/static/' % VZ_DIRECTORY
MEDIA_ROOT = '/home/webapp/%s/media/' % VZ_DIRECTORY
BACKUP_ROOT = '/home/webapp/%s/backup/' % VZ_DIRECTORY

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webapp',
        'USER': 'webapp',
        'PASSWORD': '%DBPASSWORD%',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 60,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/home/webapp/%s/django_errors.log' % VZ_DIRECTORY,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': ['file'],
            'level': 'ERROR',
        }
    },
}

