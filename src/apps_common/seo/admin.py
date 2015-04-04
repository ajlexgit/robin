from django import forms
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from suit.widgets import AutosizedTextarea
from .models import SeoConfig


class SeoConfigForm(forms.ModelForm):
    class Meta:
        model = SeoConfig
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-xxlarge',
            }),
            'keywords': AutosizedTextarea(attrs={
                'class': 'input-xxlarge',
                'rows': 3,
            }),
            'description': AutosizedTextarea(attrs={
                'class': 'input-xxlarge',
                'rows': 3,
            }),
        }


@admin.register(SeoConfig)
class SeoConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    form = SeoConfigForm