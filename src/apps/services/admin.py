from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from suit.admin import SortableModelAdmin
from seo.admin import SeoModelAdminMixin
from .models import ServicesConfig, Service


@admin.register(ServicesConfig)
class ServicesConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
    )


@admin.register(Service)
class ServiceAdmin(SeoModelAdminMixin, SortableModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'slug', 'description', 'text',
            ),
        }),
    )
    sortable = 'sort_order'
    prepopulated_fields = {
        'slug': ('title', ),
    }
    suit_form_tabs = (
        ('general', _('General')),
    )
