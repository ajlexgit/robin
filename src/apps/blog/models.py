from django.db import models
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from ckeditor.fields import CKEditorUploadField
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.autoslug import AutoSlugField
from libs.stdimage.fields import StdImageField
from libs.storages.media_storage import MediaStorage


class BlogConfig(SingletonModel):
    """ Главная страница """
    header = models.CharField(_('header'), max_length=255)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('Settings')

    def get_absolute_url(self):
        return resolve_url('blog:index')

    def __str__(self):
        return self.header


class TagQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def active(self):
        """ Выборка тэгов, в которых есть видимые посты """
        return self.filter(
            posts__status=BlogPost.STATUS_PUBLIC,
            posts__date__lte=now()
        ).order_by('pk', 'sort_order').distinct('pk')


class Tag(models.Model):
    """ Тэг """
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    sort_order = models.IntegerField(_('order'), default=0)

    objects = TagQuerySet.as_manager()

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('sort_order', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('blog:tag', tag_slug=self.slug)


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
    """ Пост """
    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PUBLIC, _('Public')),
    )

    header = models.CharField(_('header'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='header', unique=True)
    note = models.TextField(_('note'))
    text = CKEditorUploadField(_('text'))
    date = models.DateTimeField(_('publication date'), default=now)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_DRAFT)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), related_name='posts')

    preview = StdImageField(_('preview'),
        blank=True,
        storage=MediaStorage('blog/preview'),
        min_dimensions=(900, 500),
        admin_variation='admin',
        crop_area=True,
        aspects=('normal',),
        variations=dict(
            normal=dict(
                size=(900, 500),
            ),
            mobile=dict(
                size=(540, 300),
            ),
            admin=dict(
                size=(450, 250),
            ),
        ),
    )

    updated = models.DateTimeField(_('change date'), auto_now=True)
    objects = BlogPostQuerySet.as_manager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-date', '-id')

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return resolve_url('blog:detail', slug=self.slug)
