from django import forms
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableStackedInline, SortableTabularInline
from project.admin import ModelAdminInlineMixin
from libs.autocomplete.forms import AutocompleteField
from .models import AttachableBlock


class AttachableBlockRefForm(forms.ModelForm):
    block = AutocompleteField(
        label=_('Block'),
        queryset=AttachableBlock.objects.all(),
        dependencies=(('block_model', '__prefix__-block_model', False), ),
        expressions="label__icontains",
        minimum_input_length=0,
    )

    class Meta:
        widgets = {
            'block_model': forms.Select,
        }


class AttachableBlockRefTabularInline(ModelAdminInlineMixin, SortableTabularInline):
    form = AttachableBlockRefForm
    fields = ('block_model', 'block')
    extra = 0


class AttachableBlockRefStackedInline(ModelAdminInlineMixin, SortableStackedInline):
    form = AttachableBlockRefForm
    fields = ('block_model', 'block')
    extra = 0
