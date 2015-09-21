import re
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
PREVENT_CACHING = getattr(settings, 'SCC_PREVENT_CACHING', False)
MAX_AGE_PUBLIC = getattr(settings, 'SCC_MAX_AGE_PUBLIC', 86400)
MAX_AGE_PRIVATE = getattr(settings, 'SCC_MAX_AGE_PRIVATE', 0)
ENABLED = getattr(settings, 'SCC_ENABLED', True)

CACHE_URLS = []
for url_settings in getattr(settings, 'SCC_CUSTOM_CACHE_CONTROLS', []):
    CACHE_URLS.append((
        re.compile(url_settings[0]),
        url_settings[1],
        url_settings[2],
    ))


class SCCMiddleware:
    @staticmethod
    def process_response(request, response):
        if not ENABLED:
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

        if PREVENT_CACHING:
            if 'last-modified' in response:
                logger.debug('Last-modified: %s', response['last-modified'])
                del response['last-modified']
            if 'etag' in response:
                logger.debug('ETag: %s', response['etag'])
                del response['etag']

        return response