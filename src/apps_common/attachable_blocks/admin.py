from django import forms
from django.core import checks
from django.contrib.contenttypes.admin import (
    GenericTabularInline, GenericStackedInline, BaseGenericInlineFormSet
)
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableTabularInlineBase
from project.admin import ModelAdminInlineMixin
from libs.autocomplete.forms import AutocompleteField
from .models import AttachableBlock, AttachableReference


class AttachableReferenceForm(forms.ModelForm):
    block = AutocompleteField(
        label=_('Block'),
        queryset=AttachableBlock.objects.all(),
        dependencies=(('block_type', '__prefix__-block_type', False), ),
        expressions="label__icontains",
        minimum_input_length=0,
    )

    class Meta:
        fields = '__all__'
        widgets = {
            'block_type': forms.Select(attrs={
                'class': 'input-medium',
            })
        }


class AttachableReferenceFormset(BaseGenericInlineFormSet):
    """ Формсет, устанавливающий объектам set_name """
    @property
    def empty_form(self):
        form = super().empty_form
        form.instance.set_name = self.set_name
        return form

    def save_new(self, form, commit=True):
        setattr(form.instance, 'set_name', self.set_name)
        return super().save_new(form, commit)

    def save_existing(self, form, instance, commit=True):
        setattr(form.instance, 'set_name', self.set_name)
        return super().save_existing(form, instance, commit)


class BaseAttachableReferenceMixin(ModelAdminInlineMixin, SortableTabularInlineBase):
    """ Базовый класс inline-моделей """
    form = AttachableReferenceForm
    formset = AttachableReferenceFormset
    model = AttachableReference
    fields = ('block_type', 'block', 'set_name')
    readonly_fields = ('set_name',)
    extra = 0
    sortable = 'sort_order'
    set_name = 'default'

    @classmethod
    def check(cls, model, **kwargs):
        errors = super().check(model, **kwargs)
        errors.extend(cls._check_set_name(model, **kwargs))
        return errors

    @classmethod
    def _check_set_name(cls, model, **kwargs):
        if not cls.set_name:
            return [
                checks.Error(
                    'set_name can\'t be empty',
                    obj=cls
                )
            ]
        else:
            return []

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        FormSet.set_name = self.set_name
        return FormSet

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(set_name=self.set_name)


class AttachableReferenceTabularInline(BaseAttachableReferenceMixin, GenericTabularInline):
    """ Родительская модель для tabular инлайнов """
    pass


class AttachableReferenceStackedInline(BaseAttachableReferenceMixin, GenericStackedInline):
    """ Родительская модель для stacked инлайнов """
    pass
