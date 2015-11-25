from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from libs.autoslug import AutoSlugField
from ckeditor.fields import CKEditorUploadField


class NewsPageConfig(SingletonModel):
    header = models.CharField(_('header'), max_length=128)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('news:index')


class Post(models.Model):
    title = models.CharField(_('title'), max_length=128)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    text = CKEditorUploadField(_('text'), editor_options=settings.CKEDITOR_CONFIG_DEFAULT)
    is_visible = models.BooleanField(_('visible'), default=False)

    created = models.DateTimeField(_('create date'), default=now, editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('news:detail', slug=self.slug)


