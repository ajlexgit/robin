import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from libs.media_storage import MediaStorage


def generate_filepath(instance, filename):
    """ Генерация пути сохранения файла """
    return instance.generate_filename(os.path.basename(filename))


class PageFile(models.Model):
    """ Модель файла на страницу """
    STORAGE_LOCATION = None

    file = models.FileField(_('file'),
        storage=MediaStorage(),
        upload_to=generate_filepath,
        max_length=150,
    )
    displayed_name = models.CharField(_('display name'),
        max_length=150,
        blank=True,
        help_text=_('If you leave it empty the file name will be used')
    )
    sort_order = models.PositiveIntegerField(_('sort order'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        ordering = ('sort_order', )
        abstract = True

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

        super().save(*args, **kwargs)
