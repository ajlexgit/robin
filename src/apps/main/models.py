from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from gallery import *


class ImageItem(GalleryImageItem):
    STORAGE_LOCATION = 'main/gallery'
    MIN_DIMENSIONS = (1400, 1050)
    ADMIN_CLIENT_RESIZE = True

    SHOW_VARIATION = 'normal'
    ADMIN_VARIATION = 'normal'
    ASPECTS = 'normal'
    VARIATIONS = dict(
        wide=dict(
            size=(1920, 1440),
            stretch=True,
        ),
        normal=dict(
            size=(1024, 768),
        ),
        mobile=dict(
            size=(800, 600),
        ),
        admin=dict(
            size=(200, 150),
        ),
    )


class Gallery(GalleryBase):
    IMAGE_MODEL = ImageItem


class MainPageConfig(SingletonModel):
    """ Главная страница """
    gallery = GalleryField(Gallery, verbose_name=_('gallery'), blank=True, null=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('index')

    def __str__(self):
        return ugettext('Main page')
