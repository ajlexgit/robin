import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from libs.stdimage import StdImageField
from libs.media_storage import MediaStorage
from . import options


def generate_tag(instance, random_param=False):
    normal_data = {
        'src': instance.photo.on_page.url_nocache if random_param else instance.photo.on_page.url,
        'width': instance.photo.on_page.width,
        'height': instance.photo.on_page.height,
    }

    return """<img data-id="{0.id}" alt=""
         src="{1[src]}"
         width="{1[width]}"
         height="{1[height]}">""".format(instance, normal_data)


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
        storage = MediaStorage('page_photos'),
        upload_to = page_photo_filename,
        blank = True,
        admin_variation = 'admin_thumbnail',
        min_dimensions = options.PHOTOS_IN_TEXT_SIZE,
        crop_area = True,
        aspects = 'on_page',
        variations = dict(
            on_page=dict(
                size=options.PHOTOS_IN_TEXT_SIZE,
                format='JPEG',
            ),
            admin_thumbnail=dict(
                size=options.PHOTOS_ADMIN_SIZE,
            ),
        ))

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return _('Image #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }


class SimplePhoto(models.Model):
    """ Модель фото на страницу """
    app_name = models.CharField(_('application'), max_length=30, blank=True)
    model_name = models.CharField(_('model'), max_length=30, blank=True)
    instance_id = models.IntegerField(_('entry id'), db_index=True, default=0)
    photo = StdImageField(_('image'),
        storage = MediaStorage('simple_photos'),
        upload_to = page_photo_filename,
        blank = True,
        admin_variation = 'admin_thumbnail',
        max_source_dimensions = options.SIMPLE_PHOTOS_MAX_SIZE,
        variations = dict(
            admin_thumbnail=dict(
                size=options.PHOTOS_ADMIN_SIZE,
                crop=False,
                stretch=False,
            ),
        )
    )

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return _('Image #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }

