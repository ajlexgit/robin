from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from suit.widgets import AutosizedTextarea
from google_maps import GoogleCoordsField, GoogleCoordsAdminWidget
from libs.color_field import ColorField, ColorFormField, ColorOpacityField, ColorOpacityFormField
from libs.stdimage import StdImageField, StdImageAdminWidget
from libs.valute_field import ValuteField, ValuteFormField
from libs.widgets import SplitDateTimeWidget, TimeWidget, URLWidget


class BaseModelAdminMixin:
    formfield_overrides = {
        models.CharField: {
            'widget': forms.TextInput(attrs={
                'class': 'full-width',
            })
        },
        models.EmailField: {
            'widget': forms.EmailInput(attrs={
                'class': 'input-xlarge',
            })
        },
        models.URLField: {
            'widget': URLWidget(attrs={
                'class': 'full-width',
            })
        },
        models.TextField: {
            'widget': AutosizedTextarea(attrs={
                'class': 'full-width',
                'rows': 2,
            })
        },
        models.DateTimeField: {
            'widget': SplitDateTimeWidget
        },
        models.TimeField: {
            'widget': TimeWidget
        },
        StdImageField: {
            'widget': StdImageAdminWidget
        },
        ColorField: {
            'form_class': ColorFormField
        },
        ColorOpacityField: {
            'form_class': ColorOpacityFormField
        },
        ValuteField: {
            'form_class': ValuteFormField
        },
        GoogleCoordsField: {
            'widget': GoogleCoordsAdminWidget
        },
    }

    # поля, которые отображаются только для суперюзера
    superuser_fields = ()

    # поля, которые может редактировать только суперюзер.
    # Для других, поля будут readonly
    superuser_editable_fields = ()

    def get_readonly_fields(self, request, obj=None):
        """
            Блокировка полей, перечисленных в superuser_editable
        """
        fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            fields = tuple(fields) + tuple(self.superuser_editable_fields)
        return fields

    def get_fields(self, request, obj=None):
        """
            Скрытие полей, перечисленных в superuser_fields
        """
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in self.superuser_fields]
        return fields

    def get_fieldsets(self, request, obj=None):
        """
            Скрытие полей, перечисленных в superuser_fields
        """
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            for name, opts in fieldsets:
                opts['fields'] = tuple(field for field in opts['fields'] if field not in self.superuser_fields)
        return fieldsets


class ModelAdminInlineMixin(BaseModelAdminMixin):
    pass


class ModelAdminMixin(BaseModelAdminMixin):
    actions_on_top = True
    actions_on_bottom = True

    add_form_template = 'suit/change_form.html'
    change_form_template = 'suit/change_form.html'

    @property
    def media(self):
        return super().media + forms.Media(
            js=(
                'admin/js/jquery-ui.min.js',
                'common/js/jquery.cookie.js',
                'common/js/jquery.ajax_csrf.js',
                'common/js/jquery.mousewheel.js',
                'common/js/jquery.utils.js',
                'common/js/file_dropper.js',
                'admin/js/button_filter.js',
            ),
            css={
                'all': (
                    'admin/css/jquery-ui/jquery-ui.min.css',
                )
            }
        )

    def suit_cell_attributes(self, obj, column):
        """ Классы для ячеек списка """
        if column == 'view':
            return {
                'class': 'mini-column'
            }
        else:
            return {}

    def get_suit_form_tabs(self, request, add=False):
        """ Получение вкладок для модели админки Suit """
        return getattr(self, 'suit_form_tabs', ())

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """ Получаем вкладки Suit и передаем их в шаблон """
        suit_tabs = self.get_suit_form_tabs(request, add)
        context['suit_tabs'] = suit_tabs
        return super().render_change_form(request, context, add, change, form_url, obj)

    def view(self, obj):
        """ Ссылка просмотра на сайте для отображения в списке сущностей """
        if hasattr(obj, 'get_absolute_url'):
            admin_url = obj.get_absolute_url()
            if admin_url:
                return ('<a href="%s" target="_blank" title="%s">'
                        '   <span class="icon-eye-open icon-alpha75"></span>'
                        '</a>') % (admin_url, _('View on site'))
        return '<span>-//-</span>'
    view.short_description = '#'
    view.allow_tags = True