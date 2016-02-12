from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from gallery import *


class ImageItem(GalleryImageItem):
    STORAGE_LOCATION = 'main/gallery'
    MIN_DIMENSIONS = (1200, 900)
    ADMIN_CLIENT_RESIZE = True

    SHOW_VARIATION = 'normal'
    ADMIN_VARIATION = 'admin'
    ASPECTS = 'normal'
    VARIATIONS = dict(
        wide=dict(
            size=(1920, 1440),
            stretch=True,
        ),
        normal=dict(
            size=(1200, 900),
        ),
        mobile=dict(
            size=(800, 600),
        ),
        preview=dict(
            size=(200, 150),
        ),
        admin=dict(
            size=(160, 120),
        ),
    )


class VideoItem(GalleryVideoLinkItem):
    STORAGE_LOCATION = 'main/gallery'
    ADMIN_VARIATION = 'admin'
    VARIATIONS = dict(
        wide=dict(
            size=(1024, 576),
            stretch=True,
        ),
        normal=dict(
            size=(640, 480),
            stretch=True,
        ),
        mobile=dict(
            size=(480, 360),
        ),
        preview=dict(
            size=(200, 150),
        ),
        admin=dict(
            size=(160, 120),
        ),
    )


class Gallery(GalleryBase):
    IMAGE_MODEL = ImageItem
    VIDEO_LINK_MODEL = VideoItem


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
