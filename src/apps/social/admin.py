from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from .models import SocialConfig, FollowUsBlock


@admin.register(SocialConfig)
class SocialConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    """ Настройки соцкнопок """
    fieldsets = (
        (None, {
            'fields': (
                'header',
            ),
        }),
        (_('Networks'), {
            'fields': (
                'facebook', 'twitter', 'youtube',
            ),
        }),
    )


@admin.register(FollowUsBlock)
class FollowUsBlockAdmin(ModelAdminMixin, admin.ModelAdmin):
    """ Подключаемый блок соцкнопок """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('label', 'visible'),
        }),
    )
    list_display = ('label', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
    )
