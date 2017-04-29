from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class SitemapConfig(SingletonModel):
    header = models.CharField(_('header'), max_length=255)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        default_permissions = ('change', )
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('sitemap:index')
