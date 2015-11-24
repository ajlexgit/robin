from django.db import models
from django.utils.translation import ugettext_lazy as _
from attachable_blocks.models import AttachableBlock


class SampleBlock(AttachableBlock):
    BLOCK_VIEW = 'blocks.views.sample_block_render'

    title = models.CharField(_('title'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Sample block')
        verbose_name_plural = _("Sample blocks")
