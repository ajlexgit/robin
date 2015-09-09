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
    def _check_views(cls):
        errors = []
        if cls == AttachableBlock:
            return errors

        if not cls.BLOCK_VIEW:
            errors.append(
                checks.Error(
                    "attachable block '%s' has no BLOCK_VIEW" % cls.__name__,
                )
            )
        elif not get_block_view(cls):
            errors.append(
                checks.Error(
                    "Invalid BLOCK_VIEW for block '%s': '%s'" % (cls.__name__, cls.BLOCK_VIEW),
                )
            )
        return errors

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_views())
        return errors


class AttachableBlockRef(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    block_type = models.CharField(_('block type'), max_length=255, choices=get_block_choices())
    block = models.ForeignKey(AttachableBlock, verbose_name=_('block'))
    frame = models.PositiveSmallIntegerField(_('frame'), default=0)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('Block reference')
        verbose_name_plural = _('Block references')
        ordering = ('frame', 'order')
        unique_together = ('content_type', 'object_id', 'block_type', 'block')
