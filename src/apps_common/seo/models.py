from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.contenttypes.models import ContentType
from solo.models import SingletonModel
from libs.storages import MediaStorage


class SeoConfig(SingletonModel):
    title = models.CharField(_('site title'), max_length=128)
    keywords = models.TextField(_('site keywords'), max_length=255, blank=True)
    description = models.TextField(_('site description'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Defaults')

    def __str__(self):
        return ugettext('Defaults')


class SeoData(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = generic.GenericForeignKey()

    title = models.CharField(_('title'), max_length=128, blank=True)
    keywords = models.TextField(_('keywords'), max_length=255, blank=True)
    description = models.TextField(_('description'), max_length=255, blank=True)
    canonical = models.URLField(_('canonical URL'), blank=True)

    # opengraph
    og_title = models.CharField(_('title'), max_length=255, blank=True)
    og_image = models.ImageField(_('image'), blank=True, storage=MediaStorage('seo'))
    og_description = models.TextField(_('description'), blank=True)

    header = models.CharField(_('header'), max_length=128, blank=True)
    text = models.TextField(_('text'), blank=True)

    class Meta:
        default_permissions = ('change', )
        verbose_name = _('SEO data')
        verbose_name_plural = _('SEO data')
        unique_together = ('content_type', 'object_id')

    def __str__(self):
        return 'SeoData for %s(#%s)' % (self.content_type.name, self.object_id)


class Redirect(models.Model):
    old_path = models.CharField(_('redirect from'), max_length=200, unique=True,
        help_text=_("This should be an absolute path, excluding the domain name. Example: '/events/search/'."))
    new_path = models.CharField(_('redirect to'), max_length=200, blank=True,
        help_text=_("This can be either an absolute path (as above) or a full URL starting with 'http://'."))
    permanent = models.BooleanField(_('permanent'), default=True)
    created = models.DateField(_('created'), default=now, editable=False)

    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        ordering = ('old_path',)

    def __str__(self):
        return '(%s) "%s" → "%s"' % (
            '301' if self.permanent else '302',
            self.old_path,
            self.new_path,
        )


class Counter(models.Model):
    POSITION = (
        ('head', _('Inside <head>')),
        ('body_top', _('Start of <body>')),
        ('body_bottom', _('End of <body>')),
    )

    label = models.CharField(_('label'), max_length=128)
    position = models.CharField(_('position'), max_length=12, choices=POSITION)
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = _('counter')
        verbose_name_plural = _('counters')

    def __str__(self):
        return self.label


class Robots(models.Model):
    text = models.TextField(_('text'), blank=True)

    class Meta:
        managed = False
        verbose_name = _('file')
        verbose_name_plural = _('robots.txt')
        default_permissions = ()

    def __str__(self):
        return 'robots.txt'
