from settings.common import *

DOMAIN = 'directlinedev.com'
VZ_DIRECTORY = 'directlinedev.com'

# Имя хоста (имя виртуальной машины - master, staging и т.д.), должно быть настроено на виртуалке
# Метка %HOSTNAME% при развёртывании заменяется на настоящее имя виртуалки
HOSTNAME = '%HOSTNAME%'

SESSION_COOKIE_DOMAIN = '.%s' % DOMAIN

# Метка %SECRET_KEY% при развёртывании заменяется на нужный секретный ключ
SECRET_KEY = '%SECRET_KEY%'

ALLOWED_HOSTS = (
    '.%s' % DOMAIN,
)

DEBUG = False

TEMPLATE_DEBUG = False

# настройки статики
STATIC_ROOT = '/home/webapp/%s/static/' % VZ_DIRECTORY
MEDIA_ROOT = '/home/webapp/%s/media/' % VZ_DIRECTORY

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'directlinedev',
        'USER': 'webapp',
        'PASSWORD': 'kWDQs2tL4SUzgbkU',
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

