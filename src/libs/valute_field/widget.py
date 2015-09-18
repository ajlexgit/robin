from suit.widgets import EnclosedInput
from .formatters import get_formatter


class ValuteWidget(EnclosedInput):
    input_type = 'number'

    def __init__(self, *args, **kwargs):
        attrs = dict(kwargs, **get_formatter().widget_attrs)
        super().__init__(*args, **attrs)