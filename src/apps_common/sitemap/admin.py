from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from .models import SitemapConfig


@admin.register(SitemapConfig)
class SitemapConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title',
            ),
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'
