from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class SeoConfig(SingletonModel):
    title = models.CharField(_('Site title'), max_length=64)
    keywords = models.CharField(_('Site keywords'), max_length=255, blank=True)
    description = models.CharField(_('Site description'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Site config')