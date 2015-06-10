from datetime import time
from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html, smart_urlquote
from django.forms.utils import flatatt, to_current_timezone
from suit.widgets import SuitDateWidget, HTML5Input


class LinkWidget(forms.Widget):
    """ Виджет простой ссылки """
    def __init__(self, href, text, attrs=None):
        super().__init__(attrs=attrs)
        self.text = text
        self.attrs['href'] = smart_urlquote(href)
        self.attrs.setdefault('target', '_self')

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        return format_html(
            '<a {0}>{1}</a>',
            flatatt(final_attrs), self.text
        )


class URLWidget(forms.URLInput):
    """ Виджет УРЛА """

    def __init__(self, attrs=None):
        final_attrs = {'class': 'vURLField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None):
        html = super().render(name, value, attrs)
        if value:
            value = force_text(self._format_value(value))
            final_attrs = {
                'href': smart_urlquote(value),
                'target': '_blank'
            }
            html = format_html(
                '<p class="url">{0} <a{1}>{2}</a><br />{3}</p>',
                _('Currently:'), flatatt(final_attrs), value,
                html
            )
        return html


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
