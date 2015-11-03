from django.forms import widgets
from django.conf import settings
from suit.widgets import EnclosedInput


# Дополнительные настройки виджета в зависимости от языка
WIDGET_SETTINGS = {
    ('ru',): {
        'append': 'руб.'
    },
    ('en',): {
        'prepend': '$'
    }
}

for langs, value in WIDGET_SETTINGS.items():
    if settings.SHORT_LANGUAGE_CODE in langs:
        widget_kwargs = value
        break
else:
    widget_kwargs = {}



class ValuteWidget(EnclosedInput, widgets.NumberInput):
    input_type = 'number'

    def __init__(self, *args, **kwargs):
        attrs = dict(kwargs, **widget_kwargs)
        super().__init__(*args, **attrs)