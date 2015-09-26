from django.db import models
from django.core import checks
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .register import get_block_choices
from .utils import get_block_type, get_block_view


class AttachableBlock(models.Model):
    """ Базовый класс блоков """
    BLOCK_VIEW = ''

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

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_views(**kwargs))
        return errors

    @classmethod
    def _check_views(cls, **kwargs):
        if cls == AttachableBlock:
            return []

        if not cls.BLOCK_VIEW:
            return [
                checks.Error(
                    'BLOCK_VIEW is required',
                    obj=cls
                )
            ]
        elif not get_block_view(cls):
            return [
                checks.Error(
                    'BLOCK_VIEW not found',
                    obj=cls
                )
            ]
        else:
            return []


class AttachableReference(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    block_type = models.CharField(_('block type'), max_length=255, choices=get_block_choices())
    block = models.ForeignKey(AttachableBlock, verbose_name=_('block'), related_name='references')
    set_name = models.CharField(_('set name'), max_length=32, default='default')
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)

    class Meta:
        verbose_name = _('Attached block')
        verbose_name_plural = _('Attached blocks')
        ordering = ('set_name', 'sort_order')
        unique_together = ('content_type', 'object_id', 'block_type', 'block', 'set_name')
        index_together = (('content_type', 'object_id', 'set_name'), )
