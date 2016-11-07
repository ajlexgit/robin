from django.conf import settings

CACHEBLOCK_BACKEND = getattr(settings, 'CACHEBLOCK_BACKEND', 'default')
CACHEBLOCK_ENABLED = getattr(settings, 'CACHEBLOCK_ENABLED', not settings.DEBUG)

# Безопасный интервал времени, гарантирующий что на момент запроса блока,
# он будет присутствовать в кэше
CACHEBLOCK_GAP = getattr(settings, 'CACHEBLOCK_GAP', 60)

CACHEBLOCK_CSS_CLASS = 'cacheblock-block'
