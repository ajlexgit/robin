import os
import re
import sys
from celery.schedules import crontab
from django.utils.translation import ugettext_lazy as _


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

    # 'haystack',
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

    # Libs
    'libs.autocomplete',
    'libs.away',
    'libs.js_storage',
    'libs.management',
    'libs.opengraph',
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
                'Address',
                'Message',
                'ContactsConfig',
            )
        },
        '-',
        {
            'icon': 'icon-lock',
            'label': 'Authentication and Authorization',
            'permissions': 'users.admin_menu',
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
                'Counter',
                'Robots',
            ),
        },
    ),
}


# Pipeline
SASS_INCLUDE_DIR = BASE_DIR + '/static/scss/'
PIPELINE = {
    'PIPELINE_ENABLED': True,
    'COMPILERS': (
        'libs.sassc.SASSCCompiler',
    ),
    'SASS_BINARY': '/usr/bin/env sassc --load-path ' + SASS_INCLUDE_DIR,
    'SASS_ARGUMENTS': '-t compressed',
    'CSS_COMPRESSOR': 'libs.cssmin.CSSCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',

    'STYLESHEETS': {
        'core': {
            'source_filenames': (
                'scss/grid.scss',
                'scss/layout.scss',
                'scss/forms.scss',
                'scss/preloader.scss',
                'scss/text_styles.scss',

                'scss/popups/popups.scss',
                'scss/popups/preloader.scss',

                'scss/slider/slider.scss',
                'scss/slider/plugins/controls.scss',
                'scss/slider/plugins/navigation.scss',

                'contacts/scss/block.scss',
                'footer/scss/footer.scss',
                'header/scss/header.scss',
                'menu/scss/menu.scss',
            ),
            'output_filename': 'css_build/head_core.css',
        },
        'admin_customize': {
            'source_filenames': (
                'admin/scss/admin_fixes.scss',
                'admin/scss/admin_table.scss',
                'admin/scss/button_filter.scss',
                'admin/scss/dl_core.scss',
                'admin/scss/dl_login.scss',
            ),
            'output_filename': 'admin/css/customize.css',
        },
        'main_page': {
            'source_filenames': (
                'scss/section_slider.scss',
                'gallery/scss/gallery_popup.scss',
                'main/scss/index.scss',
            ),
            'output_filename': 'css_build/main_page.css',
        },
        'error_page': {
            'source_filenames': (
                'scss/error_page.scss',
            ),
            'output_filename': 'css_build/error_page.css',
        },
        'contacts_page': {
            'source_filenames': (
                'contacts/scss/index.scss',
            ),
            'output_filename': 'css_build/contacts_page.css',
        },
        'blog_page': {
            'source_filenames': (
                'paginator/scss/paginator.scss',
                'blog/scss/index.scss',
            ),
            'output_filename': 'css_build/blog_page.css',
        },
        'blog_detail_page': {
            'source_filenames': (
                'blog/scss/detail.scss',
            ),
            'output_filename': 'css_build/blog_detail_page.css',
        },
    },

    'JAVASCRIPT': {
        'core': {
            'source_filenames': (
                'polyfills/modernizr.js',
                'js/jquery-2.2.1.min.js',
                'js/jquery-ui-effects.js',

                'common/js/jquery.cookie.js',
                'common/js/jquery.utils.js',
                'common/js/jquery.ajax_csrf.js',

                'js/jquery.fitvids.js',
                'js/jquery.scrollTo.js',
                'js/drager.js',

                'js/popups/jquery.popups.js',
                'js/popups/preloader.js',
                'js/slider/slider.js',
                'js/slider/plugins/side_animation.js',
                'js/slider/plugins/fade_animation.js',
                'js/slider/plugins/autoscroll.js',
                'js/slider/plugins/navigation.js',
                'js/slider/plugins/controls.js',
                'js/slider/plugins/drag.js',
                'js/text_styles.js',

                'attachable_blocks/js/async_blocks.js',
                'contacts/js/block.js',
                'menu/js/menu.js',
            ),
            'output_filename': 'js_build/core.js',
        },
        'main_page': {
            'source_filenames': (
                'js/slider/win_height_slider.js',
                'js/jquery.youtube.js',
                'js/jquery.vimeo.js',
                'gallery/js/gallery_popup.js',
                'main/js/index.js',
            ),
            'output_filename': 'js_build/main_page.js',
        },
        'contacts_page': {
            'source_filenames': (
                'google_maps/js/core.js',
                'contacts/js/index.js',
            ),
            'output_filename': 'js_build/contacts_page.js',
        },
        'blog_page': {
            'source_filenames': (
                'blog/js/index.js',
            ),
            'output_filename': 'js_build/blog_page.js',
        },
        'blog_detail_page': {
            'source_filenames': (
                'blog/js/detail.js',
            ),
            'output_filename': 'js_build/blog_detail_page.js',
        },
    }
}

MIDDLEWARE_CLASSES = (
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'libs.js_storage.middleware.JSStorageMiddleware',
    'libs.opengraph.middleware.OpengraphMiddleware',
    'libs.cache.middleware.SCCMiddleware',
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

# Домен для куки CSRF (".example.com")
CSRF_COOKIE_DOMAIN = None

# Домен для куки сессий (".example.com")
SESSION_COOKIE_DOMAIN = None
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 30 * 24 * 3600

# Список скомпилированных регулярных выражений
# запретных юзер-агентов
DISALLOWED_USER_AGENTS = ()


# ==================================================================
# ==================== APPS SETTINGS ===============================
# ==================================================================

# Admin Dump
BACKUP_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'backup'))

# Директория для robots.txt и других открытых файлов
PUBLIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'public'))

# Youtube Data API
# для ckeditor, videolink_field, youtube
YOUTUBE_APIKEY = 'AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg'

# Smart Cache-Control
SCC_ENABLED = True
SCC_MAX_AGE_PRIVATE = 0
SCC_MAX_AGE_PUBLIC = 21600
SCC_DISABLED_URLS = [
    r'/admin/',
    r'/dladmin/',
]

#   Форматы вывода валют ValuteField в зависимости от языка
#    decimal_places     - кол-во чисел после запятой
#    decimal_mark       - разделитель целого и частного
#    thousands          - разделитель тысячных разрядов
#    trail              - не выводить дробную часть, если в ней только нули
#    utf_format         - формат с использованием UTF-символов
#    alternative_format - формат без использования UTF-символов
#    widget_attrs       - дополнительные параметры виждета
VALUTE_FORMATS = {
    ('ru',): {
        'decimal_places': 2,
        'decimal_mark': '.',
        'thousands': ' ',
        'trail': True,

        'utf_format': '{}\u20bd',
        'alternative_format': '{} руб.',
        'widget_attrs': {
            'append': 'руб.',
        },
    },
    ('en',): {
        'decimal_places': 2,
        'decimal_mark': '.',
        'thousands': ',',
        'trail': False,

        'utf_format': '${}',
        'alternative_format': '${}',
        'widget_attrs': {
            'prepend': '$',
        },
    }
}


# ==================================================================
# ==================== END APPS SETTINGS ===========================
# ==================================================================


# Cache
CACHES = {
    'default': {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:0",
        "KEY_PREFIX": LANGUAGE_CODE + SECRET_KEY,
        "OPTIONS": {
            "CLIENT_CLASS": 'redis_cache.client.DefaultClient',
            "PASSWORD": "",
        }
    }
}

# Celery
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ('pickle', 'json')
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYBEAT_SCHEDULE = {
    # создание бэкапа дважды в месяц
    'make_backup': {
        'task': 'project.tasks.make_backup',
        'schedule': crontab(day_of_month='1,15', hour='9', minute='0'),
        'kwargs': {
            'max_count': 10,
        }
    },

    # очистка старых логов
    'clean_admin_log': {
        'task': 'project.tasks.clean_admin_log',
        'schedule': crontab(day_of_month='1', hour='9', minute='0'),
        'kwargs': {
            'days': 90,
        }
    },
}

# # Haystack
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'directlinedev-haystack',
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
