from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.utils import unquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from .models import SeoConfig, SeoData, Counter


@admin.register(SeoConfig)
class SeoConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    pass


class CounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'seo'


@admin.register(Counter)
class CounterAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = CounterForm
    list_display = ('__str__', 'position')


class SeoDataAdmin(ModelAdminInlineMixin, admin.ModelAdmin):
    model = SeoData
    fieldsets = (
        (_('SEO common'), {
            'fields': ('title', 'keywords', 'description', ),
        }),
        (_('SEO text'), {
            'fields': ('header', 'text',),
        }),
        (_('Opengraph'), {
            'fields': ('og_title', 'og_image', 'og_description'),
        }),
    )


class SeoModelAdminMixin:
    """
        Модель админки, добавляющая к форме блок сео-текстов
    """
    suit_seo_position = 'top'
    suit_seo_tab = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_includes = getattr(self, 'suit_form_includes', ())
        self.suit_form_includes = default_includes + (
            ('seo/admin/admin_include.html', self.suit_seo_position, self.suit_seo_tab),
        )

    def change_view(self, request, object_id, *args, **kwargs):
        if object_id is None:
            entity = None
        else:
            entity = self.get_object(request, unquote(object_id))

        model = SeoData
        model_admin = SeoDataAdmin(model, admin.site)
        content_type = ContentType.objects.get_for_model(self.model)

        try:
            obj = model.objects.get(
                content_type=content_type,
                object_id=object_id,
            )
        except (model.DoesNotExist, model.MultipleObjectsReturned):
            obj = None

        add = obj is None
        ModelForm = model_admin.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj, prefix='seo')
            if form.has_changed():
                if form.is_valid():
                    new_object = model_admin.save_form(request, form, change=not add)
                    new_object.title = new_object.title.strip()
                    new_object.keywords = new_object.keywords.strip()
                    new_object.description = new_object.description.strip()
                    new_object.entity = entity
                    model_admin.save_model(request, new_object, form, not add)
        else:
            if obj is None:
                initial = {
                    'content_type': content_type,
                    'object_id': object_id,
                }
                initial.update(model_admin.get_changeform_initial_data(request))
                form = ModelForm(initial=initial, prefix='seo')
            else:
                form = ModelForm(instance=obj, prefix='seo')

        seoDataForm = helpers.AdminForm(
            form,
            list(model_admin.get_fieldsets(request, obj)),
            model_admin.get_prepopulated_fields(request, obj),
            model_admin.get_readonly_fields(request, obj),
            model_admin=model_admin)

        extra_context = kwargs.pop('extra_context', None) or {}
        kwargs['extra_context'] = dict(extra_context, **{
            'seoDataForm': seoDataForm,
        })
        return super().change_view(request, object_id, *args, **kwargs)
