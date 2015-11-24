from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import MainBlockFirst, MainBlockSecond


@admin.register(MainBlockFirst)
class MainBlockFirstAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')


@admin.register(MainBlockSecond)
class MainBlockSecondAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')
