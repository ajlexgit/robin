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
    def save(self, name, content, save=True, old_value=None):
        super().save(name, content, save=save)
        if old_value and old_value != self.name:
            self.storage.delete(old_value)
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

    def save_form_data(self, instance, data):
        old_value = self.value_from_object(instance)
        setattr(instance, '_%s' % self.attname, old_value)
        super().save_form_data(instance, data)

    def pre_save(self, model_instance, add):
        file = super(models.FileField, self).pre_save(model_instance, add)
        if file and not file._committed:
            old_value = getattr(model_instance, '_%s' % self.attname, None)
            file.save(file.name, file, save=False, old_value=old_value)
        return file


class ImageField(FileFieldMixin, models.ImageField):
    attr_class = ImageFieldFile
