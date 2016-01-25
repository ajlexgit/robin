from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from suit.widgets import AutosizedTextarea
from google_maps import GoogleCoordsField, GoogleCoordsAdminWidget
from libs.color_field import ColorField, ColorFormField, ColorOpacityField, ColorOpacityFormField
from libs.stdimage import StdImageField, StdImageAdminWidget
from libs.valute_field import ValuteField, ValuteFormField
from libs.widgets import SplitDateTimeWidget, TimeWidget, URLWidget


class ModelAdminInlineMixin:
    formfield_overrides = {
        models.CharField: {
            'widget': forms.TextInput(attrs={
                'class': 'full-width',
            })
        },
        models.EmailField: {
            'widget': forms.EmailInput(attrs={
                'class': 'full-width',
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
                'rows': 3,
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


class ModelAdminMixin(ModelAdminInlineMixin):
    actions_on_top = True
    actions_on_bottom = True

    add_form_template = 'suit/change_form.html'
    change_form_template = 'suit/change_form.html'

    def get_suit_form_tabs(self, request, add=False):
        """ Получение вкладок для модели админки Suit """
        return self.suit_form_tabs

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

    @property
    def media(self):
        return super().media + forms.Media(
            js = (
                'admin/js/jquery-ui.min.js',
                'common/js/jquery.cookie.js',
                'common/js/jquery.ajax_csrf.js',
                'common/js/jquery.mousewheel.js',
                'common/js/jquery.utils.js',
                'common/js/file_dropper.js',
                'admin/js/button_filter.js',
            ),
            css = {
                'all': (
                    'admin/css/jquery-ui/jquery-ui.min.css',
                    'admin/css/admin_fixes.css',
                    'admin/css/button_filter.css',
                )
            }
        )
