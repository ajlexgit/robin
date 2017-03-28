import os
from django.db import models
from django.conf import settings
from django.db.models import signals
from django.db.models.fields import files

# Фикс обновления кэша в django-solo
try:
    from solo.models import SingletonModel

    HAS_SOLO_CACHE = getattr(settings, 'SOLO_CACHE', None) is not None
except ImportError:
    HAS_SOLO_CACHE = False


class FieldFileMixin:
    def save(self, name, content, save=True):
        old_name = self.name and os.path.normpath(self.name)
        super().save(name, content, save=save)
        new_name = os.path.normpath(self.name)
        if old_name and old_name != new_name and os.path.isfile(old_name):
            self.storage.delete(old_name)
    save.alters_data = True


class FieldFile(FieldFileMixin, files.FieldFile):
    pass


class ImageFieldFile(FieldFileMixin, files.ImageFieldFile):
    pass


class FileFieldMixin:
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        signals.post_save.connect(self._post_save, sender=cls)
        signals.post_delete.connect(self._post_delete, sender=cls)

    def _post_save(self, instance, **kwargs):
        # Fix for django-solo cache
        if HAS_SOLO_CACHE and isinstance(instance, SingletonModel):
            instance.set_to_cache()

    def _post_delete(self, instance, **kwargs):
        field_file = self.value_from_object(instance)
        field_file.delete(save=False)


class FileField(FileFieldMixin, models.FileField):
    attr_class = FieldFile


class ImageField(FileFieldMixin, models.ImageField):
    attr_class = ImageFieldFile
