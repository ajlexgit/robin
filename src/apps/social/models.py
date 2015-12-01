from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from attachable_blocks.models import AttachableBlock


class SocialConfig(SingletonModel):
    header = models.CharField(_('header'), max_length=128, blank=True)
    facebook = models.URLField(_('facebook'), blank=True)
    twitter = models.URLField(_('twitter'), blank=True)
    youtube = models.URLField(_('youtube'), blank=True)

    class Meta:
        verbose_name = _('Settings')


class FollowUsBlock(AttachableBlock):
    BLOCK_VIEW = 'social.views.follow_us_render'

    class Meta:
        verbose_name = _('Follow us')
        verbose_name_plural = _('Follow us')

    def __str__(self):
        return 'Block "Follow us"'
