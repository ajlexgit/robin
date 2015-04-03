import os
import datetime
from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from libs.now import now
from libs.stdimage import *
from libs.autoslug import AutoSlugField
from libs.media_storage import MediaStorage
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.ckeditor import CKEditorField, CKEditorUploadField
from files import PageFile
from gallery import GalleryField, GalleryBase, GalleryImageItem, GalleryVideoLinkItem
from . import options

__all__ = ['Post', 'PostSection', 'PostGallery', 'PostFile']


class PostQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        # visible
        visible = kwargs.pop('visible', None)
        if visible is True:
            qs &= models.Q(status=Post.STATUS_PUBLIC, date__lte=now())
        return qs


class PostSection(models.Model):
    title = models.CharField(_('title'), max_length=100)
    alias = AutoSlugField(_('alias'),
        populate_from='title',
        unique=True,
    )

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    def __str__(self):
        return self.title


class PostGalleryImageItem(GalleryImageItem):
    STORAGE_LOCATION = options.GALLERY_PATH
    MIN_DIMENSIONS = options.GALLERY_NORMAL
    ADMIN_CLIENT_RESIZE = True

    SHOW_VARIATION = 'normal'
    ADMIN_VARIATION = 'micro'
    ASPECTS = 'small'
    VARIATIONS = dict(
        normal=dict(
            size=options.GALLERY_NORMAL,
            watermark=dict(
                file='img/watermark.png',
                padding=(20, 20),
                opacity=0.6,
            ),
        ),
        small=dict(
            size=options.GALLERY_SMALL,
            watermark=dict(
                file='img/watermark.png',
                padding=(10, 10),
                opacity=0.6,
                scale=0.4,
            ),
        ),
        micro=dict(
            size=options.GALLERY_MICRO,
        ),
    )


class PostGalleryVideoLinkItem(GalleryVideoLinkItem):
    pass


class PostGallery(GalleryBase):
    IMAGE_MODEL = PostGalleryImageItem
    VIDEO_LINK_MODEL = PostGalleryVideoLinkItem


def post_preview_filename(instance, filename):
    """ Разбиваем превьюхи по папкам по 1000 файлов максимум """
    directory = ''
    if instance.pk:
        directory = '%04d' % (instance.pk // 1000)
    return os.path.join(directory, os.path.basename(filename))


class Post(models.Model):
    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PUBLIC, _('Public')),
    )
    
    sections = models.ManyToManyField(PostSection, verbose_name=_('sections'))
    title = models.CharField(_('title'), max_length=100)
    alias = AutoSlugField(_('alias'),
        populate_from='title',
        unique=True,
    )
    preview = StdImageField(_('preview'),
        storage = MediaStorage(options.PREVIEW_PATH),
        upload_to = post_preview_filename,
        blank = True,
        admin_variation = 'normal',
        min_dimensions = options.PREVIEW_NORMAL,
        crop_area = True,
        aspects = 'normal',
        variations = dict(
            big=dict(
                size=options.PREVIEW_BIG,
                action=ACTION_STRETCH_BY_WIDTH,
                watermark=dict(
                    file='img/watermark.png',
                    padding=(20, 20),
                    opacity=0.6,
                ),
            ),
            normal=dict(
                size=options.PREVIEW_NORMAL,
            ),
            small=dict(
                size=options.PREVIEW_SMALL,
            ),
        ),
    )
    note = CKEditorField(_('note'), editor_options=settings.CKEDITOR_CONFIG_MINI)
    text = CKEditorUploadField(_('text'), editor_options=settings.CKEDITOR_CONFIG_DEFAULT)
    date = models.DateTimeField(_('date'), default=datetime.datetime.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        blank=True,
        null=True,
    )
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_DRAFT)
    gallery = GalleryField(PostGallery, verbose_name=_('gallery'), blank=True, null=True, related_name='post_gallery')

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-date', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('posts:detail', post_id=self.id)


class PostFile(PageFile):
    STORAGE_LOCATION = options.FILES_PATH

    post = models.ForeignKey(Post, verbose_name=_('post'), related_name='files')

    def generate_filename(self, filename):
        return '%d/%s' % (self.post.pk, filename)
