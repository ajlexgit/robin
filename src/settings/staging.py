from settings.common import *

DOMAIN = 'project.dev.direktweb.ru'
VZ_DIRECTORY = '/home/webapp/project.dev.direktweb.ru'

SESSION_COOKIE_DOMAIN = DOMAIN
CSRF_COOKIE_DOMAIN = DOMAIN

# Метка %SECRET_KEY% при развёртывании заменяется на нужный секретный ключ
SECRET_KEY = '%SECRET_KEY%'

ALLOWED_HOSTS = (
    DOMAIN,
)

# настройки статики
STATIC_ROOT = os.path.join(VZ_DIRECTORY, 'static')
MEDIA_ROOT = os.path.join(VZ_DIRECTORY, 'media')
BACKUP_ROOT = os.path.join(VZ_DIRECTORY, 'backup')
PUBLIC_DIR = os.path.join(VZ_DIRECTORY, 'public')

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
            'filename': os.path.join(VZ_DIRECTORY, 'django_errors.log'),
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
            'propagate': True,
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['file'],
            'level': 'ERROR',
        }
    },
}

