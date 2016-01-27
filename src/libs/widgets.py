from datetime import time
from django import forms
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


class URLWidget(forms.URLInput):
    """ Виджет URL """
    def append(self, value):
        if value:
            output = '<a href="{href}" class="add-on" target="_blank"><i class="icon-globe"></i></a>'
            return format_html(output, href=smart_urlquote(value))
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
        widgets = (SuitDateWidget(attrs=attrs),
                   HTML5Input(attrs={'class': 'input-small'}, input_type='time'))
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return ' '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0, second=0)]
        return [None, None]


class TimeWidget(forms.widgets.Input):
    """ Виджет времени """
    input_type = 'time'

    def __init__(self, attrs=None):
        final_attrs = {'class': 'input-mini'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None):
        if isinstance(value, time):
            value = value.strftime('%H:%M')
        return super().render(name, value, attrs)
