from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from ckeditor.fields import CKEditorUploadField
from libs.autoslug import AutoSlugField


class ServicesConfig(SingletonModel):
    """ Главная страница """
    header = models.CharField(_('header'), max_length=255)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('services:index')

    def __str__(self):
        return self.header


class Service(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)

    description = models.TextField(_('short description'), max_length=1024)
    text = CKEditorUploadField(_('text'))
    sort_order = models.PositiveIntegerField(_('order'), default=0)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        ordering = ('sort_order', )

    def get_absolute_url(self):
        return resolve_url('services:detail', slug=self.slug)

    def __str__(self):
        return self.title
