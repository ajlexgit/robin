from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from gallery import *
from libs.media_storage import MediaStorage
from libs.stdimage.fields import StdImageField


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
            size=(375, 250),
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
            size=(1280, 720),
            stretch=True,
        ),
        normal=dict(
            size=(1024, 576),
            stretch=True,
        ),
        mobile=dict(
            size=(800, 450),
            stretch=True,
        ),
        preview=dict(
            size=(375, 250),
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
    preview = StdImageField(_('preview'),
        blank=True,
        storage=MediaStorage('main'),
        min_dimensions=(800, 600),
        admin_variation='admin',
        crop_area=True,
        aspects=('normal',),
        variations=dict(
            normal=dict(
                size=(800, 600),
            ),
            admin=dict(
                size=(280, 280),
            ),
        ),
    )

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('index')

    def __str__(self):
        return ugettext('Main page')
