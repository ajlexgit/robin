from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import BaseStorageFinder


class PipelineFinder(BaseStorageFinder):
    storage = staticfiles_storage

    def find(self, *args, **kwargs):
        if settings.DEBUG or not settings.PIPELINE_ENABLED:
            return super().find(*args, **kwargs)
        else:
            return []

    def list(self, ignore_patterns):
        return []