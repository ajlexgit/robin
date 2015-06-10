from django import forms
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.templatetags.admin_static import static
from suit.widgets import AutosizedTextarea
from libs.widgets import SplitDateTimeWidget, TimeWidget, URLWidget


class ModelAdminInlineMixin:
    formfield_overrides = {
        models.CharField: {
            'widget': forms.TextInput(attrs={
                'class': 'input-xxlarge',
            })
        },
        models.URLField: {
            'widget': URLWidget(attrs={
                'class': 'input-xxlarge',
            })
        },
        models.TextField: {
            'widget': AutosizedTextarea(attrs={
                'class': 'input-xxlarge',
                'rows': 3,
            })
        },
        models.DateTimeField: {
            'widget': SplitDateTimeWidget
        },
        models.TimeField: {
            'widget': TimeWidget
        },
    }


class ModelAdminMixin(ModelAdminInlineMixin):
    ADDITION_JS = (
        'admin/js/jquery-ui.min.js',
        'admin/js/jquery.cookie.js',
        'admin/js/ajax_csrf.js',
    )
    ADDITION_CSS = {
        'all': (
            'admin/css/jquery-ui/jquery-ui.min.css',
            'admin/css/admin_fixes.css',
        )
    }

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
        """
            Дает возможность указать скрипты и стили,
            добавляемые по умолчанию в админке
        """
        extra = '' if settings.DEBUG else '.min'
        js = [
            'core.js',
            'admin/RelatedObjectLookups.js',
            'jquery%s.js' % extra,
            'jquery.init.js'
        ]
        if self.actions is not None:
            js.append('actions%s.js' % extra)
        if self.prepopulated_fields:
            js.extend(['urlify.js', 'prepopulate%s.js' % extra])
        return forms.Media(
            js=[static('admin/js/%s' % url) for url in js] +
               [static(url) for url in self.ADDITION_JS],
            css=self.ADDITION_CSS
        )
