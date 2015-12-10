from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from gallery import *
from libs.media_storage import MediaStorage
from libs.stdimage import StdImageField


class ImageItem(GalleryImageItem):
    STORAGE_LOCATION = 'main/gallery'
    MIN_DIMENSIONS = (400, 300)
    ADMIN_CLIENT_RESIZE = True

    SHOW_VARIATION = 'normal'
    ADMIN_VARIATION = 'normal'
    ASPECTS = 'normal'
    VARIATIONS = dict(
        normal=dict(
            size=(400, 300)
        ),
        micro=dict(
            size=(120, 100),
        ),
    )


class Gallery(GalleryBase):
    IMAGE_MODEL = ImageItem


class MainPageConfig(SingletonModel):
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
    gallery = GalleryField(Gallery, verbose_name=_('gallery'), blank=True, null=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('index')

