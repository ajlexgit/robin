from django import forms
from .widget import ValuteWidget


class ValuteFormField(forms.DecimalField):
    widget = ValuteWidget

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'class': 'input-small'
        })
        return attrs