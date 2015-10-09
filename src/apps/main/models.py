from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from attachable_blocks import AttachableBlock
from ckeditor import CKEditorUploadField
from gallery import *
from files import PageFile
from google_maps import GoogleCoordsField
from libs.color_field import ColorField, ColorOpacityField
from libs.valute_field import ValuteField
from libs.videolink_field import VideoLinkField
from libs.media_storage import MediaStorage
from libs.stdimage import StdImageField


class MainGalleryImageItem(GalleryImageItem):
    STORAGE_LOCATION = 'main/gallery'
    MIN_DIMENSIONS = (768, 576)
    ADMIN_CLIENT_RESIZE = True

    SHOW_VARIATION = 'normal'
    ADMIN_VARIATION = 'small'
    ASPECTS = 'normal'
    VARIATIONS = dict(
        normal=dict(
            size=(768, 576),
        ),
        small=dict(
            size=(160, 120),
        ),
    )

class MainGalleryVideoLinkItem(GalleryVideoLinkItem):
    STORAGE_LOCATION = 'main/gallery'
    ADMIN_VARIATION = 'small'
    VARIATIONS = dict(
        normal=dict(
            size=(640, 360),
        ),
        small=dict(
            size=(160, 120),
        ),
    )


class MainGallery(GalleryBase):
    IMAGE_MODEL = MainGalleryImageItem
    VIDEO_LINK_MODEL = MainGalleryVideoLinkItem


class MainPageConfig(SingletonModel):
    header_title = models.CharField('title', max_length=255)
    header_background = StdImageField(_('background'),
        storage=MediaStorage('main/header'),
        min_dimensions=(1024, 500),
        admin_variation='admin',
        crop_area=True,
        variations=dict(
            desktop=dict(
                size=(1024, 0),
            ),
            mobile=dict(
                size=(768, 0),
            ),
            admin=dict(
                size=(360, 270),
            ),
        ),
    )
    header_video = models.FileField(_('video'), blank=True, storage=MediaStorage('main/header'))

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
    preview2 = StdImageField(_('preview'),
        storage=MediaStorage('main/preview2'),
        min_dimensions=(100, 100),
        admin_variation='normal',
        crop_area=True,
        aspects=('normal',),
        variations=dict(
            normal=dict(
                size=(200, 200),
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
    coords = GoogleCoordsField(_('coords'), blank=True)
    gallery = GalleryField(MainGallery,
        verbose_name=_('gallery'),
        blank=True,
        null=True,
    )
    video = VideoLinkField(_('video'), blank=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('index')


class ListItem(models.Model):
    STATUS_PAID = 1
    STATUS_NOT_PAID = 2
    STATUS_DELETED = 3
    STATUSES = (
        (STATUS_PAID, _('Paid')),
        (STATUS_NOT_PAID, _('Not paid')),
        (STATUS_DELETED, _('Deleted')),
    )

    title = models.CharField(_('title'), max_length=64)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=STATUS_NOT_PAID)
    text = CKEditorUploadField(_('text'), editor_options=settings.CKEDITOR_CONFIG_DEFAULT)

    def get_absolute_url(self):
        return resolve_url('index')


class ListItemFile(PageFile):
    STORAGE_LOCATION = 'list_files'

    item = models.ForeignKey(ListItem)


class InlineSample(models.Model):
    config = models.ForeignKey(MainPageConfig, verbose_name=_('config'))

    color = ColorOpacityField(_('color'))

    class Meta:
        verbose_name = _("Inline sample")
        verbose_name_plural = _('Inline samples')


class MainBlockFirst(AttachableBlock):
    BLOCK_VIEW = 'main.views.render_first_block'

    class Meta:
        verbose_name = _('First block')
        verbose_name_plural = _("First blocks")


class MainBlockSecond(AttachableBlock):
    BLOCK_VIEW = 'main.views.render_second_block'

    class Meta:
        verbose_name = _('Second block')
        verbose_name_plural = _("Second blocks")


class ClientFormModel(models.Model):
    title = models.CharField(_('title'), max_length=128, blank=True, default='Example')

    def __str__(self):
        return self.title


class ClientInlineFormModel(models.Model):
    form = models.ForeignKey(ClientFormModel)
    name = models.CharField(_('name'), max_length=128, default='Test')

    def __str__(self):
        return self.name