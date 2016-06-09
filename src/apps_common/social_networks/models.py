from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from libs.aliased_queryset import AliasedQuerySetMixin
from libs.description import description
from . import conf


class SocialPostQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        # for_network
        for_network = kwargs.pop('for_network', None)
        if for_network:
            qs &= models.Q(network=for_network, scheduled=True)

        return qs


class SocialPost(models.Model):
    network = models.CharField(_('social network'),
        choices=conf.ALL_NETWORKS,
        default=conf.NETWORK_FACEBOOK,
        max_length=32,
        db_index=True
    )

    text = models.TextField(_('text'))
    url = models.URLField(_('URL'))
    scheduled = models.BooleanField(_('sheduled for sharing'), default=True)

    created = models.DateTimeField(_('created on'), default=now, editable=False)
    posted = models.DateTimeField(_('posted on'), null=True, editable=False)
    objects = SocialPostQuerySet.as_manager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-scheduled', '-created', )

    def __str__(self):
        return description(self.text, 10, 60)
