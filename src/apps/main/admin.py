from django.contrib import admin
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from .models import MainPageConfig


@admin.register(MainPageConfig)
class MainPageConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    pass
