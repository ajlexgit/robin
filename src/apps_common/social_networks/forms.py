from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import SocialPost
from . import conf


class SocialPostForm(forms.ModelForm):
    network = forms.ChoiceField(
        required=True,
        label=_('Social network'),
        choices=conf.ALLOWED_NETWORKS,
        initial=SocialPost._meta.get_field('network').default,
    )

    class Meta:
        model = SocialPost
        fields = '__all__'


class AutpostForm(forms.Form):
    networks = forms.MultipleChoiceField(
        required=True,
        label=_('Social networks'),
        choices=conf.ALLOWED_NETWORKS,
        initial=SocialPost._meta.get_field('network').default,
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            'required': _('Please select at least one social network'),
        }
    )

    text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'maxlength': 1024,
            'rows': 3,
        }),
        error_messages={
            'required': _('Please enter text'),
        }
    )
