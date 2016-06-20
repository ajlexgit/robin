from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.description import description
from . import conf


class FeedPostQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        # for_network
        for_network = kwargs.pop('for_network', None)
        if for_network:
            qs &= models.Q(network=for_network, scheduled=True)

        return qs


class FeedPost(models.Model):
    network = models.CharField(_('social network'),
        choices=conf.ALL_NETWORKS,
        default=conf.NETWORK_FACEBOOK,
        max_length=32
    )

    text = models.TextField(_('text'))
    url = models.URLField(_('URL'))
    scheduled = models.BooleanField(_('sheduled for sharing'), default=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True, editable=False)
    object_id = models.PositiveIntegerField(null=True, blank=True, editable=False)
    entity = generic.GenericForeignKey(for_concrete_model=False)

    created = models.DateTimeField(_('created on'), default=now, editable=False)
    posted = models.DateTimeField(_('posted on'), null=True, editable=False)
    objects = FeedPostQuerySet.as_manager()

    class Meta:
        verbose_name = _('feed post')
        verbose_name_plural = _('feeds')
        ordering = ('-scheduled', '-created', )
        index_together = (('network', 'content_type', 'object_id'), )

    def __str__(self):
        if self.entity:
            return str(self.entity)
        else:
            return description(self.text, 10, 60)