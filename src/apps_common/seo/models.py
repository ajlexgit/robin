from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from solo.models import SingletonModel


class SeoConfig(SingletonModel):
    title = models.CharField(_('Site title'), max_length=64)
    keywords = models.CharField(_('Site keywords'), max_length=255, blank=True)
    description = models.CharField(_('Site description'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Site config')


class SeoText(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = generic.GenericForeignKey()

    text = models.TextField(_('Text'), blank=True)

    class Meta:
        verbose_name = _('SEO text')
        verbose_name_plural = _('SEO texts')
        unique_together = ('content_type', 'object_id')