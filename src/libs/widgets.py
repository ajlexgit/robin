from django import forms
from django.forms import widgets
from django.utils.html import format_html


class PhoneWidget(forms.TextInput):
    input_type = 'tel'


class ChoiceInputRenderMixin:
    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        return format_html(
            '{} <label{}> {}</label>', self.tag(attrs), label_for, self.choice_label
        )


class RadioChoiceInput(ChoiceInputRenderMixin, widgets.RadioChoiceInput):
    pass


class CheckboxChoiceInput(ChoiceInputRenderMixin , widgets.CheckboxChoiceInput):
    pass


class RadioFieldRenderer(widgets.RadioFieldRenderer):
    choice_input_class = RadioChoiceInput


class CheckboxFieldRenderer(widgets.CheckboxFieldRenderer):
    choice_input_class = CheckboxChoiceInput


class RadioSelect(forms.RadioSelect):
    """
        Аналог RadioSelect, но вместо того, чтобы <input> был внутри <label>,
        помещает <input> перед <label> (для стилизации).
    """
    renderer = RadioFieldRenderer


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
        Аналог CheckboxSelectMultiple, но вместо того, чтобы <input> был внутри <label>,
        помещает <input> перед <label> (для стилизации).
    """
    renderer = CheckboxFieldRenderer
