from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from gallery import GalleryBase, GalleryImageItem, GalleryField
from libs.ckeditor import CKEditorUploadField
from libs.color_field import ColorField, ColorOpacityField
from libs.valute_field import ValuteField
from libs.media_storage import MediaStorage
from libs.stdimage import StdImageField
from attachable_blocks import AttachableBlock, AttachableBlockRef, register_block


class MainGalleryImageItem(GalleryImageItem):
    STORAGE_LOCATION = 'main/gallery'
    MIN_DIMENSIONS = (768, 576)
    ADMIN_CLIENT_RESIZE = True

    SHOW_VARIATION = 'normal'
    ADMIN_VARIATION = 'admin'
    ASPECTS = 'normal'
    VARIATIONS = dict(
        normal=dict(
            size=(768, 576),
        ),
        small=dict(
            size=(160, 120),
        ),
        admin=dict(
            size=(160, 120),
        ),
    )


class MainGallery(GalleryBase):
    IMAGE_MODEL = MainGalleryImageItem


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
    color2 = ColorOpacityField(_('color2'), blank=True)
    price = ValuteField(_('price'),
        validators=[MinValueValidator(0)]
    )
    gallery = GalleryField(MainGallery, verbose_name=_('gallery'), blank=True, null=True)

    blocks = models.ManyToManyField(AttachableBlock,
        symmetrical=False,
        through='MainPageBlockRef',
    )
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('index')


@register_block(name='First block type')
class MainBlockFirst(AttachableBlock):
    class Meta:
        verbose_name_plural = _("First blocks")


@register_block(name='Second block type')
class MainBlockSecond(AttachableBlock):
    class Meta:
        verbose_name_plural = _("Second blocks")


class MainPageBlockRef(AttachableBlockRef):
    page = models.ForeignKey(MainPageConfig)

    class Meta(AttachableBlockRef.Meta):
        unique_together = ('block_model', 'page')


class InlineSample(models.Model):
    config = models.ForeignKey(MainPageConfig, verbose_name=_('config'))

    color = ColorOpacityField(_('color'))

    class Meta:
        verbose_name = _("Inline sample")
        verbose_name_plural = _('Inline samples')
