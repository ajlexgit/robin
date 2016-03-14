from settings.common import *

DOMAIN = 'directlinedev.com'
VZ_DIRECTORY = 'directlinedev.com'

# Имя хоста (имя виртуальной машины - master, staging и т.д.), должно быть настроено на виртуалке
# Метка %HOSTNAME% при развёртывании заменяется на настоящее имя виртуалки
HOSTNAME = '%HOSTNAME%'

SESSION_COOKIE_DOMAIN = '.%s' % DOMAIN
CSRF_COOKIE_DOMAIN = '.%s' % DOMAIN

# Метка %SECRET_KEY% при развёртывании заменяется на нужный секретный ключ
SECRET_KEY = '%SECRET_KEY%'

ALLOWED_HOSTS = (
    '.%s' % DOMAIN,
)

# настройки статики
STATIC_ROOT = '/home/webapp/%s/static/' % VZ_DIRECTORY
MEDIA_ROOT = '/home/webapp/%s/media/' % VZ_DIRECTORY
BACKUP_ROOT = '/home/webapp/%s/backup/' % VZ_DIRECTORY

PIPELINE['CSS_COMPRESSOR'] = 'libs.cssmin.CSSCompressor'
PIPELINE['COMPRESSOR'] = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE['SASS_ARGUMENTS'] = '-t compressed'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'directlinedev',
        'USER': 'webapp',
        'PASSWORD': '%DBPASSWORD%',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 60,
    }
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_PREFIX = 'session'

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
