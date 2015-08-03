import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from libs.media_storage import MediaStorage
from .fields import RemovableFileField


def generate_filepath(instance, filename):
    """ Генерация пути сохранения файла """
    return instance.generate_filename(os.path.basename(filename))


class PageFile(models.Model):
    """ Модель файла на страницу """
    STORAGE_LOCATION = None

    file = RemovableFileField(storage=MediaStorage(), upload_to=generate_filepath, max_length=150, verbose_name=_('file'))
    displayed_name = models.CharField(max_length=150, verbose_name=_('display name'), blank=True,
                                      help_text=_('If you leave it empty the file name will be used'))
    order = models.PositiveIntegerField(verbose_name=_('order'), blank=True, default=0)

    class Meta:
        abstract = True
        ordering = ('order', )
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __init__(self, *args, **kwargs):
        field = self._meta.get_field('file')
        if self.STORAGE_LOCATION:
            field.storage.set_directory(self.STORAGE_LOCATION)
        super().__init__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.displayed_name

    def save(self, *args, **kwargs):
        # Если не задано отображаемое имя - устанавливаем равным имени файла
        if not self.displayed_name:
            self.displayed_name = os.path.basename(self.file.path)

        # Удаление старого файла
        if self.pk is not None:
            original = self._default_manager.get(pk=self.pk)
            if original.file != self.file:
                original.file.delete()

        super().save(*args, **kwargs)

