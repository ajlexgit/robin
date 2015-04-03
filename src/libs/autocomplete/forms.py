from django import forms
from django.utils.translation import ugettext_lazy as _
from .widgets import AutocompleteWidget, AutocompleteMultipleWidget


class AutocompleteMixin:
    def __init__(self, *args,
                 dependencies=(),
                 expressions='title__icontains',
                 placeholder=_('Search element'),
                 stringify_method='__str__',
                 minimum_input_length=2,
                 close_on_select=True,
                 **kwargs):
        """
        Параметры:
            dependencies: list/tuple
                Список кортежей из трех элементов:
                    1) имя поля в FK-модели (ключ фильтра)
                    2) имя поля для получения значения (значение фильтра).
                       Если автокомплит находится в inline-форме, то: 
                         a) на поле основной формы можно сослаться просто указав имя поля ("myfield"). 
                         b) на поле из той же inline-формы можно сослаться, добавив "__prefix__" к имени 
                            поля ("__prefix__-myfield")
                    3) является ли значение из п.2 множественным (содержащим несколько id через запятую)

            expressions: str/list/tuple (default: title__icontains)
                Условие фильтрации при частичном вводе в текстовое поле

            placeholder: str
                Заполнитель пустого значения

            stringify_method: str (default: __str__)
                Имя метода, возвращающего строковое представление объекта
                для селектбокса

            minimum_input_length: int
                Минимальное количество введенных символов для запуска
                автокомплита

            close_on_select: bool
                Закрывать список после выбора элемента
        """

        if isinstance(expressions, (list, tuple)):
            expressions = ','.join(expressions)

        self.expressions = expressions
        self.placeholder = placeholder
        self.minimum_input_length = int(minimum_input_length)
        self.close_on_select = int(bool(close_on_select))
        super().__init__(*args, **kwargs)
        self.widget.stringify_method = stringify_method
        self.widget.dependencies = dependencies

    def widget_attrs(self, widget):
        return {
            'data-placeholder': self.placeholder,
            'data-minimum_input_length': self.minimum_input_length,
            'data-close_on_select': self.close_on_select,
            'data-expressions': self.expressions,
        }


class AutocompleteField(AutocompleteMixin, forms.ModelChoiceField):
    widget = AutocompleteWidget


class AutocompleteMultipleField(AutocompleteMixin, forms.ModelMultipleChoiceField):
    widget = AutocompleteMultipleWidget

    def __init__(self, *args, **kwargs):
        # TODO: удалить в Django 1.8
        help_text = kwargs.get('help_text')
        super().__init__(*args, **kwargs)
        self.help_text = help_text

    def widget_attrs(self, widget):
        default = super().widget_attrs(widget)
        default.update({
            'data-multiple': 1,
        })
        return default

    def prepare_value(self, value):
        """ Преобразование списка в строку """
        if value is not None:
            value = ','.join(str(item) for item in value)

        return super().prepare_value(value)
