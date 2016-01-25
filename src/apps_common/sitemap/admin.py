from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from .models import SitemapConfig


@admin.register(SitemapConfig)
class SitemapConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
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
