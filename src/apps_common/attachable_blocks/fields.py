from django.db import models
from django.core import checks
from libs.autocomplete import AutocompleteWidget
from .models import AttachableBlock


def blocks_item2dict(obj):
    return {
        'id': obj.id,
        'text': obj.label
    }


class AttachableBlockField(models.ForeignKey):

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self.check_block_model(**kwargs))
        return errors

    def check_block_model(self, **kwargs):
        if not issubclass(self.rel.to, AttachableBlock):
            return [
                checks.Error(
                    'reference must be on AttachableBlock subclass',
                    obj=self,
                )
            ]
        else:
            return []

    def formfield(self, **kwargs):
        defaults = {
            'widget': AutocompleteWidget(
                expressions='label__icontains',
                minimum_input_length=0,
                item2dict_func=blocks_item2dict,
            )
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
