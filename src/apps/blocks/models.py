from django.db import models
from django.utils.translation import ugettext_lazy as _
from attachable_blocks.models import AttachableBlock


class MyBlock(AttachableBlock):
    BLOCK_VIEW = 'blocks.views.my_block_render'

    title = models.CharField(_('title'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('My block')
        verbose_name_plural = _('My blocks')

    def __str__(self):
        return '%s (Block)' % self.title

