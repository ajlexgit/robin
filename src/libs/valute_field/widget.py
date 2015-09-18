from suit.widgets import EnclosedInput
from .valute import FORMATTER


class ValuteWidget(EnclosedInput):
    input_type = 'number'

    def __init__(self, *args, **kwargs):
        attrs = dict(kwargs, **FORMATTER.widget_attrs)
        super().__init__(*args, **attrs)