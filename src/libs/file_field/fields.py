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
        newfile_attrname = '_{}_new_file'.format(self.field.name)
        setattr(self.instance, newfile_attrname, True)
        super().save(name, content, save)
    save.alters_data = True


class FileFieldMixin:
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        signals.post_save.connect(self._post_save, sender=cls)
        signals.post_delete.connect(self._post_delete, sender=cls)

    def _post_save(self, instance, **kwargs):
        # Флаг, что загружен новый файл
        new_file_attrname = '_{}_new_file'.format(self.name)
        new_file_uploaded = getattr(instance, new_file_attrname, False)
        if hasattr(instance, new_file_attrname):
            delattr(instance, new_file_attrname)

        if new_file_uploaded:
            update_fields = {}
            field_file = self.value_from_object(instance)

            source_path = self.generate_filename(instance, field_file.name)
            source_path = self.storage.get_available_name(source_path)
            with self.storage.open(field_file.name) as source:
                self.storage.save(source_path, source)

            setattr(instance, self.attname, source_path)
            update_fields[self.attname] = source_path
            self.storage.delete(field_file.name)

            queryset = instance._meta.model.objects.filter(pk=instance.pk)
            queryset.update(**update_fields)

            # Fix for django-solo cache
            if HAS_SOLO_CACHE and isinstance(instance, SingletonModel):
                instance.set_to_cache()

    def _post_delete(self, instance=None, **kwargs):
        field_file = self.value_from_object(instance)
        field_file.delete(save=False)


class FieldFile(FieldFileMixin, files.FieldFile):
    pass


class ImageFieldFile(FieldFileMixin, files.ImageFieldFile):
    pass


class FileField(FileFieldMixin, models.FileField):
    attr_class = FieldFile


class ImageField(FileFieldMixin, models.ImageField):
    attr_class = ImageFieldFile
