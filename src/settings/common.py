import os
import re
import sys
from django.utils.translation import ugettext_lazy as _
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps_common'))

SECRET_KEY = 'lr2b8&^p8dv#&b=4%op-0^2*vomo816l-*8*^5#o9@q!=zv@f$'

DEBUG = False
TEMPLATE_DEBUG = False

LANGUAGE_CODE = 'en-US'
SHORT_LANGUAGE_CODE = LANGUAGE_CODE.split('-')[0]
LANGUAGES = (
    ('ru-RU', _('Russian')),
    ('en-US', _('English')),
)

TIME_ZONE = 'America/New_York'
TIME_FORMAT = 'H:i'
DATE_FORMAT = 'E j, Y'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    'pipeline',
    'solo',
    'suit_ckeditor',

    # Apps
    'blog',
    'contacts',
    'main',
    'users',

    # Apps common
    'admin_honeypot',
    'admin_log',
    'attachable_blocks',
    'backups',
    'ckeditor',
    'footer',
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
    'HEADER_DATE_FORMAT': 'l, j F Y',

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
                'ContactBlock',
                'ContactsConfig',
            )
        },
        '-',
        '-',
        {
            'icon': 'icon-lock',
            'permissions': 'users.change_customuser',
            'label': 'Authentication and Authorization',
            'models': (
                'auth.group',
                'users.customuser',
            )
        },
        {
            'app': 'backups',
            'icon': 'icon-hdd',
        },
        {
            'app': 'admin',
            'icon': 'icon-list-alt',
            'label': _('History'),
        },
        'sites',
        {
            'app': 'seo',
            'icon': 'icon-tasks',
            'models': (
                'counter',
                'seoconfig',
            ),
        },
        '-',
        '-',
    ),
}


# Pipeline
PIPELINE_CSS = {
    'head_core': {
        'source_filenames': (
            'scss/grid.scss',
            'scss/layout.scss',
            'scss/forms.scss',
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
        'output_filename': 'css/head_core.css',
    },
    'main_page': {
        'source_filenames': (
            'scss/section_slider.scss',
            'gallery/scss/gallery_popup.scss',
            'main/scss/index.scss',
        ),
        'output_filename': 'css/main_page.css',
    },
    'error_page': {
        'source_filenames': (
            'scss/error_page.scss',
        ),
        'output_filename': 'css/error_page.css',
    },
    'contacts_page': {
        'source_filenames': (
            'contacts/scss/index.scss',
        ),
        'output_filename': 'css/contacts_page.css',
    },
    'blog_page': {
        'source_filenames': (
            'paginator/scss/paginator.scss',
            'blog/scss/index.scss',
        ),
        'output_filename': 'css/blog_page.css',
    },
    'blog_detail_page': {
        'source_filenames': (
            'blog/scss/detail.scss',
        ),
        'output_filename': 'css/blog_detail_page.css',
    },
}
PIPELINE_JS = {
    'head_core': {
        'source_filenames': (
            'js/jquery-2.1.4.min.js',
            'js/jquery-ui-effects.js',
        ),
        'output_filename': 'js/head_core.js',
    },
    'core': {
        'source_filenames': (
            'common/js/jquery.cookie.js',
            'common/js/jquery.utils.js',
            'common/js/jquery.ajax_csrf.js',
            'common/js/jquery.mousewheel.js',

            'js/jquery.fitvids.js',
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
        'output_filename': 'js/core.js',
    },
    'main_page': {
        'source_filenames': (
            'js/slider/win_height_slider.js',
            'js/jquery.youtube.js',
            'js/jquery.vimeo.js',
            'gallery/js/gallery_popup.js',
            'main/js/index.js',
        ),
        'output_filename': 'js/main_page.js',
    },
    'contacts_page': {
        'source_filenames': (
            'google_maps/js/core.js',
            'contacts/js/index.js',
        ),
        'output_filename': 'js/contacts_page.js',
    },
    'blog_page': {
        'source_filenames': (
            'blog/js/index.js',
        ),
        'output_filename': 'js/blog_page.js',
    },
    'blog_detail_page': {
        'source_filenames': (
            'blog/js/detail.js',
        ),
        'output_filename': 'js/blog_detail_page.js',
    },
}


MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
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

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:profile_self'
RESET_PASSWORD_REDIRECT_URL = 'index'
LOGOUT_URL = 'index'

SESSION_COOKIE_AGE = 30 * 24 * 3600

# Email
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@asskicker.ru'
EMAIL_HOST_PASSWORD = 'noreply66671301'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'noreply@asskicker.ru'


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

# Список скомпилированных регулярных выражений
# запретных юзер-агентов
DISALLOWED_USER_AGENTS = ()

# ==================================================================
# ==================== APPS SETTINGS ===============================
# ==================================================================

# Admin honeypot
ADMIN_HONEYPOT_EMAIL_ADMINS = False

# Autocomplete
AUTOCOMPLETE_CACHE_BACKEND = 'default'

# Admin Dump
BACKUP_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'backup'))

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
#    decimal_places   - кол-во чисел после запятой
#    decimal_mark     - разделитель целого и частного
#    thousands        - разделитель тысячных разрядов
#    utf_format       - формат с использованием UTF-символов
#    alternate_format - формат без использования UTF-символов
VALUTE_FORMATS = {
    ('ru',): {
        'decimal_places': 2,
        'decimal_mark': '.',
        'thousands': ' ',

        'trailed_format': True,
        'utf_format': '{}\u20bd',
        'alternate_format': '{} руб.',
    },
    ('en',): {
        'decimal_places': 2,
        'decimal_mark': '.',
        'thousands': ',',

        'trailed_format': False,
        'utf_format': '${}',
        'alternate_format': '${}',
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
        "KEY_PREFIX": SHORT_LANGUAGE_CODE + SECRET_KEY,
        "OPTIONS": {
            "CLIENT_CLASS": 'redis_cache.client.DefaultClient',
            "PASSWORD": "",
        }
    }
}


# Templates
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


# Locale
LOCALE_PATHS = (
    'locale',
)


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
    'libs.debug_finder.PipelineFinder',
)


# Pipeline
# pipeline ставит type для тега script равным application/javascript, что плохо для IE8
PIPELINE_MIMETYPES = (
    (b'text/coffeescript', '.coffee'),
    (b'text/less', '.less'),
    (b'text/javascript', '.js'),
    (b'text/x-sass', '.sass'),
    (b'text/x-scss', '.scss')
)
PIPELINE_CSS_COMPRESSOR = ''
PIPELINE_JS_COMPRESSOR = ''
PIPELINE_COMPILERS = (
    'libs.sassc.SASSCCompiler',
)
SASS_INCLUDE_DIR = BASE_DIR + '/static/scss/'
PIPELINE_SASS_BINARY = '/usr/bin/env sassc --load-path ' + SASS_INCLUDE_DIR
PIPELINE_SASS_ARGUMENTS = '-t nested'

# Ckeditor
CKEDITOR_CONFIG_DEFAULT = {
    'language': SHORT_LANGUAGE_CODE,
    'height': 320,
    'forcePasteAsPlainText': True,
    'extraPlugins': 'autogrow,textlen,enterfix,pagephotos,pagevideos,simplephotos',
    'autoGrow_maxHeight': '540',
    'contentsCss': (STATIC_URL + 'ckeditor/css/ckeditor.css',),
    'plugins': 'basicstyles,undo,contextmenu,'
               'elementspath,enterkey,entities,floatingspace,'
               'format,htmlwriter,justify,link,list,liststyle,'
               'removeformat,resize,'
               'showborders,sourcearea,tab,'
               'toolbar,wsc,wysiwygarea',
    'toolbar': [
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']
        },
        {
            'name': 'paragraph',
            'items': ['NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                      'JustifyBlock']
        },
        '/',
        {
            'name': 'insert',
            'items': ['PagePhotos', 'PageVideos']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'styles',
            'items': ['Format']
        },
        {
            'name': 'document',
            'items': ['Source']
        },
    ]
}
CKEDITOR_CONFIG_MINI = {
    'language': SHORT_LANGUAGE_CODE,
    'height': 100,
    'forcePasteAsPlainText': True,
    'extraPlugins': 'autogrow,textlen,enterfix',
    'autoGrow_maxHeight': '500',
    'contentsCss': (STATIC_URL + 'ckeditor/css/ckeditor.css',),
    'plugins': 'basicstyles,contextmenu,'
               'elementspath,enterkey,entities,floatingspace,'
               'htmlwriter,link,pastefromword,pastetext,'
               'removeformat,resize,showborders,sourcearea,'
               'tab,toolbar,wsc,wysiwygarea',
    'removeButtons': 'Anchor,Strike,Superscript,Subscript,JustifyBlock',
    'toolbar': [
        {
            'name': 'document',
            'items': ['Source']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']
        },
    ]
}
