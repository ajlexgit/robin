from django import forms


class MainForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=False
    )


class InlineForm(forms.Form):
    name = forms.CharField(
        label='Name',
        required=False
    )