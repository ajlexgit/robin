from django import forms
from django.core import checks
from django.core.cache import cache
from django.contrib.contenttypes.admin import (
    GenericTabularInline, GenericStackedInline, BaseGenericInlineFormSet
)
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableTabularInlineBase
from project.admin import ModelAdminInlineMixin
from libs.autocomplete import AutocompleteWidget
from .models import AttachableReference


def get_block_types():
    """
        Возвращает список content_type_id всех блоков из кэша
    """
    return cache.get('attachable_block_types')


class AttachedBlocksForm(forms.ModelForm):
    block_type = forms.ChoiceField(
        label=_('type'),
        choices=get_block_types,
    )

    class Meta:
        fields = ('block_type', 'block', 'set_name')
        widgets = {
            'block': AutocompleteWidget(
                dependencies=(('block_content_type', '__prefix__-block_type', False),),
                expressions="label__icontains",
                minimum_input_length=0,
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['block_type'] = self.instance.block.block_content_type.pk


class AttachedBlocksFormset(BaseGenericInlineFormSet):
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


class BaseAttachedBlocksMixin(ModelAdminInlineMixin, SortableTabularInlineBase):
    """ Базовый класс inline-моделей """
    form = AttachedBlocksForm
    formset = AttachedBlocksFormset
    model = AttachableReference
    # fields = ('block_type', 'block', 'set_name')
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


class AttachedBlocksTabularInline(BaseAttachedBlocksMixin, GenericTabularInline):
    """ Родительская модель для tabular инлайнов """
    pass


class AttachedBlocksStackedInline(BaseAttachedBlocksMixin, GenericStackedInline):
    """ Родительская модель для stacked инлайнов """
    pass
