from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from yandex_maps import YandexCoordsField
from google_maps import GoogleCoordsField
from solo.models import SingletonModel
from libs.media_storage import MediaStorage
from libs.stdimage.fields import StdImageField


class MainPageConfig(SingletonModel):
    header_title = models.CharField('title', max_length=255)
    preview = StdImageField(_('preview'),
        storage=MediaStorage('main/preview'),
        min_dimensions=(400, 300),
        admin_variation='admin',
        crop_area=True,
        aspects=('normal', ),
        variations=dict(
            normal=dict(
                size=(800, 600),
            ),
            admin=dict(
                size=(360, 270),
            ),
        ),
    )
    description = models.TextField(_('description'), blank=True)
    address = models.CharField(_('address'), max_length=255, blank=True)
    coords = YandexCoordsField(_('coordinates'), null=True, blank=True)
    coords2 = GoogleCoordsField(_('coordinates'), null=True, blank=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('index')