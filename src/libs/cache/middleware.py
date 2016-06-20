import re
import logging
from django.conf import settings
from django.utils.cache import patch_vary_headers

logger = logging.getLogger(__name__)
PREVENT_CACHING = getattr(settings, 'SCC_PREVENT_CACHING', settings.DEBUG)
MAX_AGE_PUBLIC = getattr(settings, 'SCC_MAX_AGE_PUBLIC', 24 * 3600)
MAX_AGE_PRIVATE = getattr(settings, 'SCC_MAX_AGE_PRIVATE', 0)
ENABLED = getattr(settings, 'SCC_ENABLED', True)

CACHE_URLS = []
for url_settings in getattr(settings, 'SCC_CUSTOM_CACHE_CONTROLS', []):
    CACHE_URLS.append((
        re.compile(url_settings[0]),
        url_settings[1],
        url_settings[2],
    ))

DISABLED_URLS = []
for url_settings in getattr(settings, 'SCC_DISABLED_URLS', []):
    DISABLED_URLS.append(re.compile(url_settings))


class SCCMiddleware:
    @staticmethod
    def process_response(request, response):
        if not ENABLED:
            return response

        # Если не указан content-type - выходим
        if 'content-type' not in response:
            return response

        # Если не HTML-страница - выходим
        content_type = response['content-type']
        is_html = 'text/html' in content_type
        is_json = 'application/json' in content_type
        if not is_html and not is_json:
            return response

        # Если нет юзера - выходим
        if not hasattr(request, 'user'):
            return response

        # Запрещенные адреса
        for url in DISABLED_URLS:
            if url.match(request.path_info):
                return response

        # Если заголовок уже установлен - не меняем его
        if 'cache-control' not in response:
            if request.user.is_authenticated():
                response['Cache-Control'] = 'private, must-revalidate, max-age={}'.format(
                    MAX_AGE_PRIVATE
                )
            else:
                response['Cache-Control'] = 'public, must-revalidate, max-age={}'.format(
                    MAX_AGE_PUBLIC
                )

            # пользовательские правила
            for url in CACHE_URLS:
                if url[0].match(request.path_info):
                    response['Cache-Control'] = '{}, must-revalidate, max-age={}'.format(*url[1:])
                    break

        # Игнорирование кэширования (при разработке)
        if PREVENT_CACHING:
            if 'last-modified' in response:
                logger.debug('Prevented "Last-modified": %s', response['last-modified'])
                del response['last-modified']
            if 'etag' in response:
                logger.debug('Prevented "ETag": %s', response['etag'])
                del response['etag']

        # Кэш должен различаться для разных кук
        patch_vary_headers(response, ('Cookie',))

        return response