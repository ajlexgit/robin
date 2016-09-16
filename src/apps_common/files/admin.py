from django import forms
from django.core import checks
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.contrib.contenttypes.admin import GenericInlineModelAdminChecks
from project.admin.base import ModelAdminInlineMixin
from suit.admin import SortableGenericStackedInline
from libs.widgets import FileWidget
from .models import PageFile


class PageFileForm(forms.ModelForm):
    class Media:
        js = (
            'files/admin/js/files.js',
        )

    class Meta:
        model = PageFile
        fields = '__all__'
        widgets = {
            'file': FileWidget(attrs={'class': 'file-on-page'}),
        }


class PageFileFormset(BaseGenericInlineFormSet):
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


class PageFileInlineMixinChecks(GenericInlineModelAdminChecks):
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


class PageFileInlineMixin(ModelAdminInlineMixin):
    """ Базовый класс inline-моделей """
    model = PageFile
    form = PageFileForm
    formset = PageFileFormset
    fields = ['file', 'name', 'downloads']
    readonly_fields = ('set_name', 'downloads')
    extra = 0
    set_name = ''

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        FormSet.set_name = self.set_name
        return FormSet

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(set_name=self.set_name)


class PageFileInline(PageFileInlineMixin, SortableGenericStackedInline):
    checks_class = PageFileInlineMixinChecks
    sortable = 'sort_order'
