from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin

from .models import RobinPageConfig





@admin.register(RobinPageConfig)
class RobinPageConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (

            ),
        }),
    )
    
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
    )
