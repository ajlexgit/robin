from django import forms
from django.core import checks
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.admin import BaseGenericInlineFormSet, GenericInlineModelAdminChecks
from suit.admin import SortableGenericTabularInline, SortableGenericStackedInline
from project.admin import ModelAdminInlineMixin
from libs.autocomplete import AutocompleteWidget
from .models import AttachableReference
from .utils import get_block_types


class AttachedBlocksForm(forms.ModelForm):
    block_type = forms.TypedChoiceField(
        coerce=int,
        label=_('Type'),
        choices=get_block_types,
    )

    class Meta:
        fields = '__all__'
        widgets = {
            'block': AutocompleteWidget(
                dependencies=(('block_content_type', '__prefix__-block_type', False),),
                expressions="label__icontains",
                minimum_input_length=0,
            ),
        }

    class Media:
        js = (
            'attachable_blocks/admin/js/related.js',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['block_type'] = self.instance.block.block_content_type.pk
        else:
            blocks = list(self.fields['block_type'].choices)
            if blocks:
                self.initial['block_type'] = blocks[0][0]


class AttachedBlocksFormset(BaseGenericInlineFormSet):
    """ Формсет, устанавливающий объектам set_name """
    @property
    def empty_form(self):
        form = super().empty_form
        form.instance.set_name = self.set_name
        return form

    def save_new(self, form, commit=True):
        setattr(form.instance, 'set_name', self.set_name)
        setattr(form.instance, 'block_ct_id', form.cleaned_data.get('block_type'))
        return super().save_new(form, commit)

    def save_existing(self, form, instance, commit=True):
        setattr(form.instance, 'set_name', self.set_name)
        setattr(form.instance, 'block_ct_id', form.cleaned_data.get('block_type'))
        return super().save_existing(form, instance, commit)


class BaseAttachedBlocksMixinChecks(GenericInlineModelAdminChecks):
    def check(self, cls, parent_model, **kwargs):
        errors = super().check(cls, parent_model, **kwargs)
        errors.extend(self._check_set_name(cls, parent_model))
        return errors

    def _check_set_name(self, cls, parent_model):
        if not cls.set_name:
            return [
                checks.Error(
                    'set_name can\'t be empty',
                    obj=cls
                )
            ]
        else:
            return []


class BaseAttachedBlocksMixin(ModelAdminInlineMixin):
    """ Базовый класс inline-моделей """
    form = AttachedBlocksForm
    formset = AttachedBlocksFormset
    model = AttachableReference
    fields = ['block_type', 'block', 'ajax']
    superuser_fields = ('ajax', )
    readonly_fields = ('set_name',)
    extra = 0
    set_name = 'default'

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        FormSet.set_name = self.set_name
        return FormSet

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(set_name=self.set_name)


class AttachedBlocksTabularInline(BaseAttachedBlocksMixin, SortableGenericTabularInline):
    """ Родительская модель для tabular инлайнов """
    checks_class = BaseAttachedBlocksMixinChecks
    sortable = 'sort_order'


class AttachedBlocksStackedInline(BaseAttachedBlocksMixin, SortableGenericStackedInline):
    """ Родительская модель для stacked инлайнов """
    checks_class = BaseAttachedBlocksMixinChecks
    sortable = 'sort_order'
