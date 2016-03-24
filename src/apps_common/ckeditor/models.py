import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from libs.stdimage import StdImageField
from libs.media_storage import MediaStorage


def page_photo_filename(instance, filename):
    """ Разбиваем картинки по папкам по 1000 файлов максимум """
    directory = ''
    if instance.pk:
        directory = '%04d' % (instance.pk // 1000)
    return os.path.join(directory, os.path.basename(filename))


class PagePhoto(models.Model):
    """ Модель фото на страницу """
    app_name = models.CharField(_('application'), max_length=30, blank=True)
    model_name = models.CharField(_('model'), max_length=30, blank=True)
    instance_id = models.IntegerField(_('entry id'), db_index=True, default=0)
    photo = StdImageField(_('image'),
        storage=MediaStorage('page_photos'),
        upload_to=page_photo_filename,
        blank=True,
        admin_variation='admin_thumbnail',
        min_dimensions=(960, 540),
        crop_area=True,
        aspects='on_page',
        variations=dict(
            wide=dict(
                size=(1440, 810)
            ),
            normal=dict(
                size=(960, 540)
            ),
            mobile=dict(
                size=(512, 288),
            ),
            admin_thumbnail=dict(
                size=(224, 126),
            ),
        ))

    class Meta:
        verbose_name = _('page photo')
        verbose_name_plural = _('page photos')
        default_permissions = ('change', )

    def __str__(self):
        return _('Image #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }


def page_file_filename(instance, filename):
    """ Разбиваем файлы по папкам по 1000 файлов максимум """
    directory = ''
    if instance.pk:
        directory = '%04d' % (instance.pk // 1000)
    return os.path.join(directory, os.path.basename(filename))


class PageFile(models.Model):
    """ Модель файла на страницу """
    app_name = models.CharField(_('application'), max_length=30, blank=True)
    model_name = models.CharField(_('model'), max_length=30, blank=True)
    instance_id = models.IntegerField(_('entry id'), db_index=True, default=0)
    file = models.FileField(_('file'),
        storage=MediaStorage('page_files'),
        upload_to=page_file_filename,
        blank=True,
    )

    class Meta:
        verbose_name = _('page file')
        verbose_name_plural = _('page files')
        default_permissions = ('change',)

    def __str__(self):
        return _('File #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }


@receiver(post_delete, sender=PageFile)
def delete_pagefile(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


class SimplePhoto(models.Model):
    """ Модель фото на страницу """
    app_name = models.CharField(_('application'), max_length=30, blank=True)
    model_name = models.CharField(_('model'), max_length=30, blank=True)
    instance_id = models.IntegerField(_('entry id'), db_index=True, default=0)
    photo = StdImageField(_('image'),
        storage=MediaStorage('simple_photos'),
        upload_to=page_photo_filename,
        blank=True,
        admin_variation='admin_thumbnail',
        max_source_dimensions=(2048, 2048),
        variations=dict(
            mobile=dict(
                size=(0, 0),
                crop=False,
                max_width=512,
            ),
            admin_thumbnail=dict(
                size=(0, 0),
                crop=False,
                max_width=250,
                max_height=250,
            ),
        )
    )

    class Meta:
        verbose_name = _('simple photo')
        verbose_name_plural = _('simple photos')
        default_permissions = ('change', )

    def __str__(self):
        return _('Image #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }

