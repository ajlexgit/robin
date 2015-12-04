from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from libs.media_storage import MediaStorage
from libs.stdimage import StdImageField


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

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('index')

