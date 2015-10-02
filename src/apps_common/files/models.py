import os
from django.db import models
from django.core import checks
from django.utils.translation import ugettext_lazy as _
from libs.media_storage import MediaStorage


def generate_filepath(instance, filename):
    """ Генерация пути сохранения файла """
    return instance.generate_filename(os.path.basename(filename))


class PageFile(models.Model):
    """ Модель файла на страницу """
    STORAGE_LOCATION = 'files'

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
        field.storage.set_directory(self.STORAGE_LOCATION)
        super().__init__(*args, **kwargs)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls.check_storage_location(**kwargs))
        return errors

    @classmethod
    def check_storage_location(cls, **kwargs):
        if not cls.STORAGE_LOCATION:
            return [
                checks.Error(
                    'STORAGE_LOCATION is empty',
                    obj=cls
                )
            ]
        elif not isinstance(cls.STORAGE_LOCATION, str):
            return [
                checks.Error(
                    'STORAGE_LOCATION must be a str object',
                    obj=cls
                )
            ]
        else:
            return []

    def __str__(self, *args, **kwargs):
        return self.displayed_name

    def save(self, *args, **kwargs):
        # Если не задано отображаемое имя - устанавливаем равным имени файла
        if not self.displayed_name:
            self.displayed_name = os.path.basename(self.file.path)

        super().save(*args, **kwargs)

    def generate_filename(self, filename):
        """
            По умолчанию файл кладется в папку [FK_ID]/[FILENAME],
            где FK_ID - ID в первом ForeignKey
        """
        foreign_fields = (
            field
            for field in self._meta.get_fields()
            if field.concrete and
               not field.auto_created and
               field.many_to_one and
               field.related_model is not None
        )
        try:
            fk_field = next(foreign_fields)
        except StopIteration:
            raise TypeError('%s has no ForeignKey relation' % self.__class__.__name__)
        return '%04d/%s' % (fk_field.value_from_object(self), filename)
