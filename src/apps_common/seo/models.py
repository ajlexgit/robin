from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from solo.models import SingletonModel


class SeoDataManager(models.Manager):
    def get_for(self, obj):
        ct = ContentType.objects.get_for_model(obj.__class__)
        return self.model.objects.get(content_type=ct, object_id=obj.pk)

    def get_or_create_for(self, obj):
        ct = ContentType.objects.get_for_model(obj.__class__)
        return self.model.objects.get_or_create(content_type=ct, object_id=obj.pk)


class SeoConfig(SingletonModel):
    title = models.CharField(_('site title'), max_length=128)
    keywords = models.TextField(_('site keywords'), max_length=255, blank=True)
    description = models.TextField(_('site description'), max_length=160, blank=True)

    class Meta:
        verbose_name = _('Site config')


class SeoData(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = generic.GenericForeignKey()

    title = models.CharField(_('title'), max_length=128, blank=True)
    keywords = models.TextField(_('keywords'), max_length=255, blank=True)
    description = models.TextField(_('description'), max_length=160, blank=True)

    header = models.CharField(_('header'), max_length=128, blank=True)
    text = models.TextField(_('text'), blank=True)

    objects = SeoDataManager()

    class Meta:
        verbose_name = _('SEO data')
        verbose_name_plural = _('SEO data')
        unique_together = ('content_type', 'object_id')

    def __str__(self):
        return 'SeoData for %s(#%s)' % (self.content_type.name, self.object_id)


class Counter(models.Model):
    POSITION = (
        ('head', 'Head'),
        ('body_top', 'Body Top'),
        ('body_bottom', 'Body Bottom'),
    )

    title = models.CharField(_('title'), max_length=128)
    position = models.CharField(_('position'), max_length=12, choices=POSITION)
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = _('counter')
        verbose_name_plural = _('counters')

    def __str__(self):
        return self.title
