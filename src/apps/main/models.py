from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from libs.ckeditor import CKEditorUploadField
from libs.color_field import ColorField
from libs.media_storage import MediaStorage
from libs.stdimage import StdImageField


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
    text = CKEditorUploadField(_('text'), editor_options=settings.CKEDITOR_CONFIG_DEFAULT)
    description = models.TextField(_('description'), blank=True)
    color = ColorField(_('color'), blank=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('index')


class InlineSample(models.Model):
    config = models.ForeignKey(MainPageConfig, verbose_name=_('config'))

    color = ColorField(_('color'))

    class Meta:
        verbose_name = _("Inline sample")
        verbose_name_plural = _('Inline samples')
