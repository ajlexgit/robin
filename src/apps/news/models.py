from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from libs.media_storage import MediaStorage
from libs.stdimage import StdImageField
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.autoslug import AutoSlugField
from ckeditor.fields import CKEditorUploadField


class NewsPageConfig(SingletonModel):
    """ Главная страница новостей """
    header = models.CharField(_('header'), max_length=128)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('news:index')


class PostQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        visible = kwargs.pop('visible', None)
        if visible is None:
            pass
        elif visible:
            qs &= models.Q(is_visible=True, publication_date__lte=now())
        else:
            qs &= ~models.Q(is_visible=True, publication_date__lte=now())

        return qs


class Post(models.Model):
    """ Новость """
    preview = StdImageField(_('preview'),
        blank=True,
        storage=MediaStorage('news/posts'),
        min_dimensions=(800, 600),
        admin_variation='normal',
        crop_area=True,
        aspects=('normal',),
        variations=dict(
            wide=dict(
                size=(800, 600),
            ),
            normal=dict(
                size=(400, 300),
            ),
            micro=dict(
                size=(40, 30),
            ),
        ),
    )
    title = models.CharField(_('title'), max_length=128)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    text = CKEditorUploadField(_('text'), editor_options=settings.CKEDITOR_CONFIG_DEFAULT)
    publication_date = models.DateTimeField(_('publication date'), default=now)
    is_visible = models.BooleanField(_('visible'), default=False)

    created = models.DateTimeField(_('create date'), default=now, editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-publication_date', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('news:detail', slug=self.slug)


