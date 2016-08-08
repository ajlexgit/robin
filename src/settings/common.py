import os
import re
import sys
from django.utils.translation import ugettext_lazy as _
from .pipeline import PIPELINE

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps_common'))

SECRET_KEY = 'lr2b8&^p8dv#&b=4%op-0^2*vomo816l-*8*^5#o9@q!=zv@f$'

DEBUG = False

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 'djcelery_email',
    'pipeline',
    'solo',
    'suit_ckeditor',

    # Apps
    'blog',
    'contacts',
    'main',
    'users',

    # Apps common
    'admin_ctr',
    'admin_honeypot',
    'admin_log',
    'attachable_blocks',
    'backups',
    'ckeditor',
    'footer',
    'form_helper',
    'gallery',
    'google_maps',
    'header',
    'menu',
    'paginator',
    'seo',
    'social_networks',

    # Libs
    'libs.ajaxcache',
    'libs.autocomplete',
    'libs.away',
    'libs.color_field',
    'libs.js_storage',
    'libs.management',
    'libs.pipeline',
    'libs.stdimage',
    'libs.templatetags',
    'libs.variation_field',
)

# Suit
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Project',

    # search
    'SEARCH_URL': '',

    # menu
    'MENU': (
        {
            'app': 'main',
            'icon': 'icon-file',
        },
        {
            'app': 'blog',
            'icon': 'icon-file',
            'models': (
                'BlogPost',
                'Tag',
                'BlogConfig',
            )
        },
        {
            'app': 'contacts',
            'icon': 'icon-file',
            'models': (
                'Message',
                'Address',
                'ContactsConfig',
            )
        },
        '-',
        {
            'app': 'social_networks',
            'icon': 'icon-lock',
            'models': (
                'SocialLinks',
                'FeedPost',
            )
        },
        '-',
        {
            'icon': 'icon-lock',
            'label': 'Authentication and Authorization',
            'permissions': 'users.change_customuser',
            'models': (
                'auth.Group',
                'users.CustomUser',
            )
        },
        {
            'app': 'backups',
            'icon': 'icon-hdd',
            'permissions': 'users.admin_menu',
        },
        {
            'app': 'admin',
            'icon': 'icon-list-alt',
            'label': _('History'),
            'permissions': 'users.admin_menu',
        },
        {
            'app': 'sites',
            'permissions': 'users.admin_menu',
        },
        {
            'app': 'seo',
            'icon': 'icon-tasks',
            'permissions': 'users.admin_menu',
            'models': (
                'SeoConfig',
                'Redirect',
                'Counter',
                'Robots',
            ),
        },
    ),
}


# Pipeline
SASS_INCLUDE_DIR = BASE_DIR + '/static/scss/'
PIPELINE['SASS_BINARY'] = '/usr/bin/env sassc --load-path ' + SASS_INCLUDE_DIR

MIDDLEWARE_CLASSES = (
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'libs.js_storage.middleware.JSStorageMiddleware',
    'libs.cache.middleware.SCCMiddleware',
    'libs.middleware.xss.XSSProtectionMiddleware',
    'libs.middleware.utm.UTMMiddleware',
    'menu.middleware.MenuMiddleware',
    'seo.middleware.RedirectMiddleware',
)

ALLOWED_HOSTS = ()

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


# Sites and users
SITE_ID = 1
ANONYMOUS_USER_ID = -1
AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'index'
LOGIN_REDIRECT_URL = 'index'
RESET_PASSWORD_REDIRECT_URL = 'index'
LOGOUT_URL = 'index'

# Email
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@automessenger.ru'
EMAIL_HOST_PASSWORD = 'woodstock1999'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'noreply@automessenger.ru'
EMAIL_SUBJECT_PREFIX = '[%s] ' % (SUIT_CONFIG['ADMIN_NAME'], )
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
# CELERY_EMAIL_TASK_CONFIG = {
#     'rate_limit': '10/m',
# }

# ==================================================================
# ==================== APPS SETTINGS ===============================
# ==================================================================

# Admin Dump
BACKUP_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'backup'))

# Директория для robots.txt и других открытых файлов
PUBLIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'public'))

# Google Map API
GOOGLE_APIKEY = 'AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg'

# Youtube Data API
# для ckeditor, videolink_field, youtube
YOUTUBE_APIKEY = 'AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg'

# Social Networks API
TWITTER_APP_ID = 'j3tkGKGYdUvJy5i97us36UEaF'
TWITTER_SECRET = '5xdxDZeQQi8mUjpQ86rtr2dMZqkSOn4wQFP4VPNlVDGGPhYV51'
TWITTER_TOKEN = '201200112-g53dkoQAgJCYxgpiMw4AMpeM8QOuyXrvm5VAh7Cu'
TWITTER_TOKEN_SECRET = '37Hc33tE6cBHIDEDEwQFaMFwPsCf3mXQABuXKuKsZiVI7'
FACEBOOK_TOKEN = 'EAADhZCRZAniwcBAONB6fBjEgG0vZAJCRir46Lpa02Yb0aOtoA' \
                 '8FIDMXOL7sJxLxptZCi7pkkC1XUi1uVIkjqZArCARcgx8ZCtKA' \
                 '7qw8Vm9C6IIKqOoOE8RTYnVigifVirZBwID4OUTZB6dyI1mVDw' \
                 'fimIJjZCyjuf2diToFYsVClwYQZDZD'
LINKEDIN_TOKEN = 'AQVDPMVg20HqmE0bJWq9pm27iFe116GKlrH9o7vHu_Xp1O89yS' \
                 'f0ilw3GZc4W_u4zNI0EUD9EfnedLfAiEJxSmansU_P6eDPU5Pq' \
                 '8oJ-33qDg_GxHw-Yi7C5DzunRuV_ab5fQxZRN8elsuukWx29kl' \
                 '_B-yamd4gOH8nHA-Uv5FESS7Ul2MM'

# Виджет Instagram
INSTAGRAM_TOKEN = '481470271.0a39b8a.872bb1e18c044e6fbadf88b9a422970b'

# Smart Cache-Control
SCC_ENABLED = True
SCC_MAX_AGE_PRIVATE = 0
SCC_MAX_AGE_PUBLIC = 24*3600
SCC_DISABLED_URLS = [
    r'/admin/',
    r'/dladmin/',
]

# Формат валют (RUB / USD / EUR / GBP)
# Для включения зависимости от языка сайта - задать None или удалить
VALUTE_FORMAT = None

# ==================================================================
# ==================== END APPS SETTINGS ===========================
# ==================================================================

# Домен для куки сессий (".example.com")
SESSION_COOKIE_DOMAIN = None
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 30 * 24 * 3600

# Домен для куки CSRF (".example.com")
CSRF_COOKIE_DOMAIN = None

# Список скомпилированных регулярных выражений
# запретных юзер-агентов
DISALLOWED_USER_AGENTS = ()

# Получатели писем о ошибках при DEBUG = False
ADMINS = (
    ('pix', 'pix666@ya.ru'),
)

# Получатели писем о битых ссылках при DEBUG=False
# Требуется подключить django.middleware.common.BrokenLinkEmailsMiddleware
MANAGERS = (
    ('pix', 'pix666@ya.ru'),
)

# Список скомпилированных регулярных выражений адресов страниц,
# сообщения о 404 на которых не должны отправляться на почту (MANAGERS)
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

# DB
DATABASES = {}

# Cache
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:0",
        "KEY_PREFIX": LANGUAGE_CODE + SECRET_KEY,
        "OPTIONS": {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
            "PASSWORD": "",
        }
    }
}

# Celery
# from celery.schedules import crontab
# BROKER_URL = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ('pickle', 'json')
# CELERY_TIMEZONE = 'Europe/Moscow'
# CELERY_SEND_TASK_ERROR_EMAILS = True
# CELERYBEAT_SCHEDULE = {
#     # создание бэкапа дважды в месяц
#     'make_backup': {
#         'task': 'project.tasks.make_backup',
#         'schedule': crontab(day_of_month='1,15', hour='9', minute='0'),
#         'kwargs': {
#             'max_count': 10,
#         }
#     },
#
#     # очистка старых логов
#     'clean_admin_log': {
#         'task': 'project.tasks.clean_admin_log',
#         'schedule': crontab(day_of_month='1', hour='9', minute='0'),
#         'kwargs': {
#             'days': 90,
#         }
#     },
# }

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            os.path.join(BASE_DIR, 'templates'),
        ),
        'OPTIONS': {
            'context_processors': (
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'google_maps.context_processors.google_apikey',
            ),
            'loaders': (
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ),
        }
    },
]

# Locale
LOCALE_PATHS = (
    'locale',
)

# Datetime formats
FORMAT_MODULE_PATH = [
    'project.formats',
]

# Media
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR + "/static/",
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)