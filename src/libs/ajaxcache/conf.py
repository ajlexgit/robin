from django.conf import settings

AJAXCACHE_BACKEND = getattr(settings, 'AJAXCACHE_BACKEND', 'default')

# Безопасный интервал времени, гарантирующий что на момент запроса блока,
# он будет присутствовать в кэше
AJAXCACHE_GAP = getattr(settings, 'AJAXCACHE_GAP', 60)

AJAXCACHE_CSS_CLASS = 'ajaxcache-block'