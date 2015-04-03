from django.conf import settings
from pipeline.storage import PipelineCachedStorage
from django.contrib.staticfiles.finders import find


class DebugPipelineCachedStorage(PipelineCachedStorage):
    """
        На локалке не работает статика при pipeline 1.4+.
        Поэтому в settings.dev нужно добавить
            STATICFILES_STORAGE = 'libs.debug_storage.DebugPipelineCachedStorage'
    """
    def path(self, name):
        return (settings.DEBUG and find(name)) or super().path(name)

    def exists(self, name):
        return (settings.DEBUG and find(name) is not None) or super().exists(name)
