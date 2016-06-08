from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from libs.description import description
from . import conf


class SocialPost(models.Model):
    network = models.CharField(_('social network'),
        choices=conf.NETWORKS,
        default=conf.NETWORK_FACEBOOK,
        max_length=32,
        db_index=True
    )

    text = models.TextField(_('text'))
    url = models.CharField(_('URL'), max_length=512, blank=True)
    image = models.CharField(_('image URL'), max_length=255, blank=True)

    created = models.DateTimeField(_('created on'), default=now, editable=False)
    modified = models.DateTimeField(_('modified on'), auto_now=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created', )

    def __str__(self):
        return description(self.text, 10, 60)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
