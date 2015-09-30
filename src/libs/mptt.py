from django.db import models
from mptt.models import MPTTModel
from mptt.admin import MPTTModelAdmin
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey
from mptt.querysets import TreeQuerySet
from suit.admin import SortableModelAdmin, SortableChangeList

__all__ = ['MPTTModel', 'TreeForeignKey', 'MPTTQuerySet', 'MPTTQuerySetManager', 'SortableMPTTModelAdmin']


# ========================
#       Fix Queryset
# ========================

class MPTTQuerySet(TreeQuerySet):
    def only(self, *fields):
        mptt_meta = self.model._mptt_meta
        mptt_fields = tuple(
            getattr(mptt_meta, key)
            for key in ('left_attr', 'right_attr', 'tree_id_attr', 'level_attr')
        )
        final_fields = set(mptt_fields + fields + tuple(mptt_meta.order_insertion_by))
        return super().only(*final_fields)


class MPTTQuerySetManager(TreeManager):
    _queryset_class = MPTTQuerySet

    def get_leafnodes(self):
        return self._mptt_filter(
            left=(models.F(self.model._mptt_meta.right_attr) - 1)
        )


# ========================
#       Fix ADMIN
# ========================

class SortableMPTTChangeList(SortableChangeList):
    def get_ordering(self, request, queryset):
        mptt_opts = self.model_admin.model._mptt_meta
        return (mptt_opts.tree_id_attr, mptt_opts.left_attr,)


class SortableMPTTModelAdmin(MPTTModelAdmin, SortableModelAdmin):
    """
        Класс для сортируемого MPTT-дерева.
        Способ, описанный в доках Suit (MPTTModelAdmin, SortableModelAdmi) - косячный.
    """
    def get_changelist(self, request, **kwargs):
        return SortableMPTTChangeList
