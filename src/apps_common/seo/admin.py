from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from .models import SeoConfig, SeoData, Counter
from .seo import Seo

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
        """ Показываем вкладку SEO, если есть права """
        default = super().get_suit_form_tabs(request, add)
        if request.user.has_perm('seo.change_seodata'):
            default = default + ((SEO_TAB_NAME, _('SEO')), )
        return default

    def get_seo_form(self, request, obj=None, change=False):
        """ Получение формы SeoData, связанной с сущностью """
        content_type = ContentType.objects.get_for_model(self.model)
        seo_model_admin = SeoDataAdmin(SeoData, self.admin_site)
        seo_instance = None
        seo_model_form_initial = {}

        if change:
            try:
                seo_instance = SeoData.objects.get(
                    content_type=content_type,
                    object_id=obj.id,
                )
            except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
                pass

        seo_model_form = seo_model_admin.get_form(request, seo_instance)
        seo_model_form_initial.update(seo_model_admin.get_changeform_initial_data(request))

        if request.method == 'POST':
            return seo_model_form(
                request.POST,
                request.FILES,
                instance=seo_instance,
                initial=seo_model_form_initial,
                prefix=SEO_FORM_PREFIX
            )
        else:
            return seo_model_form(
                instance=seo_instance,
                initial=seo_model_form_initial,
                prefix=SEO_FORM_PREFIX
            )

    def save_seo_form(self, request, obj, change=False):
        """ Сохранение формы SeoData, связанной с сущностью """
        seo_model_admin = SeoDataAdmin(SeoData, self.admin_site)
        seo_form = self.get_seo_form(request, obj, change=change)

        if seo_form.is_valid() and seo_form.has_changed():
            is_add = seo_form.instance.pk is None
            content_type = ContentType.objects.get_for_model(self.model)

            seo_instance = seo_model_admin.save_form(request, seo_form, change=not is_add)
            seo_instance.content_type = content_type
            seo_instance.object_id = obj.id
            seo_model_admin.save_model(request, seo_instance, seo_form, change=not is_add)

    def response_add(self, request, obj, *args, **kwargs):
        self.save_seo_form(request, obj, change=False)
        return super().response_add(request, obj, *args, **kwargs)

    def response_change(self, request, obj, *args, **kwargs):
        self.save_seo_form(request, obj, change=True)
        return super().response_change(request, obj, *args, **kwargs)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        seo_model_admin = SeoDataAdmin(SeoData, self.admin_site)
        seo_form = self.get_seo_form(request, obj, change=change)

        context['seoDataForm'] = helpers.AdminForm(
            seo_form,
            list(seo_model_admin.get_fieldsets(request, seo_form.instance)),
            seo_model_admin.get_prepopulated_fields(request, seo_form.instance),
            seo_model_admin.get_readonly_fields(request, seo_form.instance),
            model_admin=seo_model_admin
        )
        return super().render_change_form(request, context, add, change, form_url, obj)

    def delete_model(self, request, obj):
        """ Удаление SeoData при удалении сущности """
        content_type = ContentType.objects.get_for_model(self.model)
        seo_data = SeoData.objects.filter(
            content_type=content_type,
            object_id=obj.id,
        )

        super().delete_model(request, obj)
        seo_data.delete()

