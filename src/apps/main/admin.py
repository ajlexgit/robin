from django import forms
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from .models import MainPageConfig


class MainPageConfigForm(forms.ModelForm):
    class Meta:
        model = MainPageConfig
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-xxlarge',
            }),
        }


@admin.register(MainPageConfig)
class MainPageConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    form = MainPageConfigForm
