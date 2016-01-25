from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.utils import unquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from .models import SeoConfig, SeoData, Counter

SEO_TAB_NAME = 'seo'
SEO_FORM_PREFIX = 'seo'


@admin.register(SeoConfig)
class SeoConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    pass


class CounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = SEO_FORM_PREFIX


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


class SeoModelAdminMixin(ModelAdminMixin):
    """
        Модель админки, добавляющая к форме блок сео-текстов
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_includes = getattr(self, 'suit_form_includes', ())
        self.suit_form_includes = default_includes + (
            ('seo/admin/admin_include.html', 'top', SEO_TAB_NAME),
        )

    def get_suit_form_tabs(self, request, add=False):
        default = super().get_suit_form_tabs(request, add)
        if not add and request.user.has_perm('seo.change_seodata'):
            default = default + ((SEO_TAB_NAME, _('SEO')), )
        return default

    def change_view(self, request, object_id, *args, **kwargs):
        if object_id is None:
            entity = None
        else:
            entity = self.get_object(request, unquote(object_id))

        model = SeoData
        model_admin = SeoDataAdmin(model, admin.site)
        content_type = ContentType.objects.get_for_model(self.model)

        try:
            seo_data = model.objects.get(
                content_type=content_type,
                object_id=object_id,
            )
        except (model.DoesNotExist, model.MultipleObjectsReturned):
            seo_data = None

        add = seo_data is None
        ModelForm = model_admin.get_form(request, seo_data)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=seo_data, prefix=SEO_FORM_PREFIX)
            if form.has_changed():
                if form.is_valid():
                    new_object = model_admin.save_form(request, form, change=not add)
                    new_object.title = new_object.title.strip()
                    new_object.keywords = new_object.keywords.strip()
                    new_object.description = new_object.description.strip()
                    new_object.entity = entity
                    model_admin.save_model(request, new_object, form, not add)
        else:
            initial = {
                'content_type': content_type,
                'object_id': object_id,
            }
            initial.update(model_admin.get_changeform_initial_data(request))
            form = ModelForm(instance=seo_data, initial=initial, prefix=SEO_FORM_PREFIX)

        seoDataForm = helpers.AdminForm(
            form,
            list(model_admin.get_fieldsets(request, seo_data)),
            model_admin.get_prepopulated_fields(request, seo_data),
            model_admin.get_readonly_fields(request, seo_data),
            model_admin=model_admin)

        extra_context = kwargs.pop('extra_context', None) or {}
        kwargs['extra_context'] = dict(extra_context, **{
            'seoDataForm': seoDataForm,
        })
        return super().change_view(request, object_id, *args, **kwargs)
