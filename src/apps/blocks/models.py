from django.db import models
from django.utils.translation import ugettext_lazy as _
from attachable_blocks.models import AttachableBlock


class MainBlockFirst(AttachableBlock):
    BLOCK_VIEW = 'blocks.views.render_first_block'

    class Meta:
        verbose_name = _('First block')
        verbose_name_plural = _("First blocks")


class MainBlockSecond(AttachableBlock):
    BLOCK_VIEW = 'blocks.views.render_second_block'

    class Meta:
        verbose_name = _('Second block')
        verbose_name_plural = _("Second blocks")