from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from .models import Config


@admin.register(Config)
class ConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (_('Footer'), {
            'fields': ('email', 'phone', 'social_facebook'),
        }),
    )
