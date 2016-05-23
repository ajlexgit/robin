from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import CKEditorUploadField
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.stdimage.fields import StdImageField
from libs.storages.media_storage import MediaStorage


class BannerQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        active = kwargs.pop('active', False)
        if active is True:
            qs &= models.Q(is_visible=True, since_date__lte=now()) & (models.Q(to_date=None) | models.Q(to_date__gte=now()))

        return qs


class Banner(models.Model):
    SHOW_ALWAYS = 'always'
    SHOW_ONCE_SESSION = 'session'
    SHOW_ONCE = 'once'
    SHOW_OPTS = (
        (SHOW_ALWAYS, _('Always')),
        (SHOW_ONCE_SESSION, _('Once per session')),
        (SHOW_ONCE, _('Once per user')),
    )

    label = models.CharField(_('label'), max_length=255, help_text=_('for inner use'))
    url = models.URLField(_('url'))

    image = StdImageField(_('image'),
        storage=MediaStorage('popup_banner/image'),
        min_dimensions=(300, 300),
        admin_variation='admin',
        crop_area=True,
        aspects=('normal',),
        variations=dict(
            normal=dict(
                size=(480, 480),
            ),
            admin=dict(
                size=(200, 200),
            ),
        ),
    )
    header = models.CharField(_('header'), max_length=255, blank=True)
    text = CKEditorUploadField(_('text'), height=200, blank=True)

    timeout = models.IntegerField(_('timeout'), help_text=_('seconds from page load'), default=10)
    is_visible = models.BooleanField(_('visible'), default=True)
    show_type = models.CharField(_('show'), max_length=16, choices=SHOW_OPTS, default=SHOW_ONCE_SESSION)
    since_date = models.DateField(_('since'), default=now)
    to_date = models.DateField(_('to'), null=True, blank=True)
    objects = BannerQuerySet.as_manager()

    class Meta:
        verbose_name = _('banner')
        verbose_name_plural = _('banners')
        ordering = ('-since_date', )

    def __str__(self):
        return self.label


class PageAttachment(models.Model):
    banner = models.ForeignKey(Banner, related_name='pages')
    regex = models.CharField(_('URL Regex'), max_length=255)

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ('regex',)

    def __str__(self):
        return self.regex

