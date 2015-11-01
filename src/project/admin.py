from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from suit.widgets import AutosizedTextarea
from google_maps import GoogleCoordsField, GoogleCoordsAdminWidget
from yandex_maps import YandexCoordsField, YandexCoordsAdminWidget
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
        YandexCoordsField: {
            'widget': YandexCoordsAdminWidget
        },
    }


class ModelAdminMixin(ModelAdminInlineMixin):
    actions_on_top = True
    actions_on_bottom = True

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
                'admin/js/jquery.cookie.js',
                'admin/js/jquery.mousewheel.min.js',
                'admin/js/jquery.ajax_csrf.js',
                'admin/js/jquery.utils.js',
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
