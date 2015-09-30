from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin
from suit.widgets import AutosizedTextarea
from suit.admin import SortableModelAdmin, SortableChangeList
from libs.widgets import SplitDateTimeWidget, TimeWidget, URLWidget


class ModelAdminInlineMixin:
    formfield_overrides = {
        models.CharField: {
            'widget': forms.TextInput(attrs={
                'class': 'input-xxlarge',
            })
        },
        models.EmailField: {
            'widget': forms.EmailInput(attrs={
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
                'admin/js/ajax_csrf.js',
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


class SortableMPTTChangeList(SortableChangeList):
    def get_ordering(self, request, queryset):
        mptt_opts = self.model_admin.model._mptt_meta
        return (mptt_opts.tree_id_attr, mptt_opts.left_attr,)


class SortableMPTTModelAdmin(MPTTModelAdmin, SortableModelAdmin):
    """
        Класс для сортируемого MPTT-дерева.
        Способ, описанный в доках Suit (MPTTModelAdmin, SortableModelAdmi) - косячный.
    """
    def get_changelist(self, request, **kwargs):
        return SortableMPTTChangeList