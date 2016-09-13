import os
from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from libs.storages import MediaStorage
from .fields import PageFileFileField


def generate_filepath(instance, filename):
    """ Генерация пути сохранения файла """
    return instance.generate_filename(os.path.basename(filename))


class PageFile(models.Model):
    """ Модель файла на страницу """
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')
    file = PageFileFileField(_('file'),
        storage=MediaStorage('files'),
        upload_to=generate_filepath,
        max_length=150,
    )
    name = models.CharField(_('name'),
        max_length=150,
        blank=True,
        help_text=_('If you leave it empty the file name will be used')
    )
    downloads = models.PositiveIntegerField(_('download count'), default=0)
    set_name = models.CharField(_('set name'), max_length=32, default='default')
    sort_order = models.PositiveIntegerField(_('sort order'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        index_together = (('content_type', 'object_id', 'set_name'), )
        ordering = ('sort_order', )

    def __str__(self, *args, **kwargs):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.basename(self.file.path)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url('files:download', file_id=self.pk)

    def generate_filename(self, filename):
        if self.pk:
            return '%03d/%s' % ((self.pk // 100), filename)
        else:
            return filename
