from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from libs.now import now
from .register import get_block_choices
from .utils import get_block_type


class AttachableBlock(models.Model):
    """ Базовый класс блоков """
    block_type = models.CharField(_('block type'),
        max_length=255,
        choices=get_block_choices(),
        editable=False,
    )
    label = models.CharField(_('label'), max_length=128, help_text=_('For inner use'))
    visible = models.BooleanField(_('visible'), default=False)
    created = models.DateTimeField(_('create date'), editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('Attachable block')
        verbose_name_plural = _('Attachable blocks')
        ordering = ('label', )

    def save(self, *args, **kwargs):
        self.block_type = get_block_type(self)
        if not self.created:
            self.created = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label


class AttachableBlockRef(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    block_type = models.CharField(_('block type'), max_length=255, choices=get_block_choices())
    block = models.ForeignKey(AttachableBlock, verbose_name=_('block'))
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('Block reference')
        verbose_name_plural = _('Block references')
        ordering = ('order', )
        unique_together = ('content_type', 'object_id', 'block_type', 'block')
