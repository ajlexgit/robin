from django.db import models
from django.core import checks
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from model_utils.managers import InheritanceQuerySetMixin
from .utils import get_block_types, get_block, get_block_view


class AttachableBlockQuerySet(InheritanceQuerySetMixin, models.QuerySet):
    pass


class AttachableBlock(models.Model):
    """ Базовый класс блоков """
    BLOCK_VIEW = ''

    block_content_type = models.ForeignKey(ContentType,
        null=True,
        editable=False,
        related_name='+',
    )
    label = models.CharField(_('label'), max_length=128, help_text=_('For inner use'))
    visible = models.BooleanField(_('visible'), default=True)
    created = models.DateTimeField(_('create date'), editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    objects = AttachableBlockQuerySet.as_manager()

    class Meta:
        verbose_name = _('attachable block')
        verbose_name_plural = _('attachable blocks')
        ordering = ('label', )
        default_permissions = ()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = now()

        # content_type реальной модели блока
        # при сохранении через реальную модель блока
        if not self.block_content_type:
            if self.__class__ != AttachableBlock:
                self.block_content_type = ContentType.objects.get_for_model(self)

        super().save(*args, **kwargs)

        # content_type реальной модели блока
        # при сохранении через AttachableBlock
        if not self.block_content_type:
            block = get_block(self.pk)
            if block:
                AttachableBlock.objects.filter(pk=self.pk).update(
                    block_content_type=ContentType.objects.get_for_model(block)
                )

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
    """
        Связь экземпляра блока с экземпляром страницы
    """
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    block_ct = models.ForeignKey(ContentType, null=True, related_name='+')
    block = models.ForeignKey(AttachableBlock, verbose_name=_('block'), related_name='references')
    ajax = models.BooleanField(_('AJAX load'), default=False,
        help_text=_('load block through AJAX')
    )

    set_name = models.CharField(_('set name'), max_length=32, default='default')
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)

    class Meta:
        verbose_name = _('attached block')
        verbose_name_plural = _('attached blocks')
        ordering = ('set_name', 'sort_order')
        index_together = (('content_type', 'object_id', 'set_name'), )

    def __str__(self):
        block_type = dict(get_block_types()).get(self.block_ct_id) or 'Undefined'
        instance = '%s.%s (#%s)' % (
            self.content_type.app_label,
            self.content_type.model,
            self.object_id
        )
        return '%s (%s) → %s' % (self.block, block_type, instance)
