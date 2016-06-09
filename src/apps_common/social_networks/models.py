from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from libs.description import description
from . import conf


class SocialPost(models.Model):
    network = models.CharField(_('social network'),
        choices=conf.ALL_NETWORKS,
        default=conf.NETWORK_FACEBOOK,
        max_length=32,
        db_index=True
    )

    text = models.TextField(_('text'))
    url = models.CharField(_('URL'), max_length=512, blank=True)

    modified = models.DateTimeField(_('modified on'), default=now)
    created = models.DateTimeField(_('created on'), default=now, editable=False)
    posted = models.DateTimeField(_('posted on'), null=True, editable=False)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created', )

    def __str__(self):
        return description(self.text, 10, 60)
