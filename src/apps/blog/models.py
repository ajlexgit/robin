from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from ckeditor.fields import CKEditorUploadField
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.autoslug import AutoSlugField
from libs.media_storage import MediaStorage
from libs.stdimage.fields import StdImageField


class BlogConfig(SingletonModel):
    header = models.CharField(_('header'), max_length=255)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('blog:index')


class TagQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def active(self):
        return self.filter(
            posts__status=BlogPost.STATUS_PUBLIC,
            posts__date__lte=now()
        ).distinct('pk')


class Tag(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from=('title',), unique=True)

    objects = TagQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title


class BlogPostQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        # visible
        visible = kwargs.pop('visible', None)
        if visible is True:
            qs &= models.Q(status=BlogPost.STATUS_PUBLIC, date__lte=now())
        elif visible is False:
            qs ^= models.Q(status=BlogPost.STATUS_PUBLIC, date__lte=now())
        return qs


class BlogPost(models.Model):
    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PUBLIC, _('Public')),
    )

    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from=('title',), unique=True)
    note = models.TextField(_('note'))
    text = CKEditorUploadField(_('text'), editor_options=settings.CKEDITOR_CONFIG_DEFAULT)
    date = models.DateTimeField(_('publication date'), default=now)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_DRAFT)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), through='PostTag', related_name='posts')

    preview = StdImageField(_('preview'),
        blank=True,
        storage=MediaStorage('blog/preview'),
        min_dimensions=(1200, 600),
        admin_variation='admin',
        crop_area=True,
        aspects=('normal',),
        variations=dict(
           normal=dict(
               size=(1200, 600),
           ),
           admin=dict(
               size=(400, 200),
           ),
        ),
    )

    updated = models.DateTimeField(_('change date'), auto_now=True)

    objects = BlogPostQuerySet.as_manager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('blog:detail', slug=self.slug)


class PostTag(models.Model):
    post = models.ForeignKey(BlogPost, verbose_name=_('post'))
    tag = models.ForeignKey(Tag, verbose_name=_('tag'))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = ('post', 'tag')
