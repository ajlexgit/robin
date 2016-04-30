from django.conf import settings

AJAX_CACHE_BACKEND = getattr(settings, 'AJAX_CACHE_BACKEND', 'default')

# Безопасный интервал времени, гарантирующий что на момент запроса блока,
# он будет присутствовать в кэше
AJAX_CACHE_GAP = getattr(settings, 'AJAX_CACHE_GAP', 60)
