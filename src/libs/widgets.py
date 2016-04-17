from django import forms
from django.forms import widgets
from django.utils.encoding import force_str
from django.utils.html import format_html, smart_urlquote
from django.forms.utils import flatatt, to_current_timezone
from suit.widgets import SuitDateWidget, HTML5Input


class LinkWidget(forms.Widget):
    """ Виджет простой ссылки """
    def __init__(self, text='', attrs=None):
        super().__init__(attrs=attrs)
        self.text = str(text)
        self.attrs.setdefault('target', '_self')

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        href = smart_urlquote(value)
        text = self.text or href
        return format_html(
            '<a href="{href}" {attrs}>{text}</a>',
            href=href,
            attrs=flatatt(final_attrs),
            text=force_str(text),
        )


class ReadonlyFileWidget(forms.Widget):
    """ Виджет ссылки на файл """
    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
        self.attrs.setdefault('target', '_blank')

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        if value and hasattr(value, "url"):
            return format_html(
                '<a href="{href}" {attrs}>{text}</a>',
                href=smart_urlquote(value.url),
                attrs=flatatt(final_attrs),
                text=force_str(value),
            )
        else:
            return ''


class URLWidget(forms.URLInput):
    """ Виджет URL """
    @staticmethod
    def append(value):
        if value:
            output = '<a href="{href}" class="add-on" target="_blank"><i class="icon-globe"></i></a>'
            href = force_str(value)
            return format_html(output, href=smart_urlquote(href))
        else:
            output = '<span class="add-on"><i class="icon-globe"></i></span>'
            return format_html(output)

    def render(self, name, value, attrs=None):
        html = super().render(name, value, attrs)
        return format_html(
            '<div class="url input-append">'
            '  {html} '
            '  {append}'
            '</div>',
            html=html,
            append=self.append(value)
        )


class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    """ Виджет даты-времени """
    def __init__(self, attrs=None):
        subwidgets = (
            SuitDateWidget(attrs=attrs),
            HTML5Input(attrs={'class': 'input-small'}, input_type='time')
        )
        forms.MultiWidget.__init__(self, subwidgets, attrs)

    def format_output(self, rendered_widgets):
        return ' '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0, second=0)]
        return [None, None]


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
