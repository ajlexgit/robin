from django import forms
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableTabularInlineBase
from project.admin import ModelAdminInlineMixin
from libs.autocomplete.forms import AutocompleteField
from .models import AttachableBlock, AttachableBlockRef


class AttachableBlockRefForm(forms.ModelForm):
    block = AutocompleteField(
        label=_('Block'),
        queryset=AttachableBlock.objects.all(),
        dependencies=(('block_type', '__prefix__-block_type', False), ),
        expressions="label__icontains",
        minimum_input_length=0,
    )

    class Meta:
        widgets = {
            'block_type': forms.Select(attrs={
                'class': 'input-medium',
            }),
            'frame': forms.TextInput(attrs={
                'type': 'number',
                'class': 'input-mini',
                'min': 0,
            })
        }


class AttachableBlockRefTabularInline(ModelAdminInlineMixin, SortableTabularInlineBase, GenericTabularInline):
    form = AttachableBlockRefForm
    model = AttachableBlockRef
    fields = ('block_type', 'block', 'frame')
    extra = 0


class AttachableBlockRefStackedInline(ModelAdminInlineMixin, SortableTabularInlineBase, GenericStackedInline):
    form = AttachableBlockRefForm
    model = AttachableBlockRef
    fields = ('block_type', 'block', 'frame')
    extra = 0
