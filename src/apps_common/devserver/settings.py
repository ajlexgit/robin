from django.conf import settings

DEVSERVER_MODULES = getattr(settings, 'DEVSERVER_MODULES', (
    'devserver.modules.request.RequestModule',
    'devserver.modules.render.ProfileRenderModule',
    'devserver.modules.sql.SQLSummaryModule',
))

DEVSERVER_IGNORED_PREFIXES = getattr(settings, 'DEVSERVER_IGNORED_PREFIXES', (
    settings.STATIC_URL,
    settings.MEDIA_URL,
    '/favicon',
))
