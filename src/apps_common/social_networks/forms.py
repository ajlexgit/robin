from collections import Iterable
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

