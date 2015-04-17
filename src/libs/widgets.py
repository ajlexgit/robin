from datetime import time
from django import forms
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt, to_current_timezone
from suit.widgets import SuitDateWidget, HTML5Input


class LinkWidget(forms.Widget):
    """ Виджет простой ссылки """
    def __init__(self, href, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.attrs['href'] = href
        self.attrs.setdefault('target', '_self')

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)

        output = "<a {attrs}>{text}</a>".format(
            text=self.text,
            attrs=flatatt(final_attrs),
        )
        return mark_safe(output)


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

    def render(self, name, value, attrs=None):
        if isinstance(value, time):
            value = value.strftime('%H:%M')
        return super().render(name, value, attrs)
