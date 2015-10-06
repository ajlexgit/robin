import pickle
from django.conf import settings
from django.forms import widgets
from django.core.cache import caches
from django.forms.utils import flatatt
from django.shortcuts import resolve_url
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

CACHE_BACKEND = getattr(settings,  'AUTOCOMPLETE_CACHE_BACKEND', 'default')
cache = caches[CACHE_BACKEND]


def default_format_item(obj):
    return {
        'id': obj.pk,
        'text': str(obj),
    }


class AutocompleteWidget(widgets.Widget):
    choices = ()

    """
        Виджет для автокомплит-полей.

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

            format_item: func (default: None)
                Функция, возвращающая представление объекта для селектбокса.
                Должна вернуть словарь, который обязан включать ключи "id" и "text"

            minimum_input_length: int
                Минимальное количество введенных символов для запуска автокомплита

            close_on_select: bool
                Закрывать список после выбора элемента
    """
    class Media:
        js = (
            'autocomplete/js/autocomplete.js',
            'autocomplete/js/select2.min.js',
            'autocomplete/js/select2_locale_%s.js' % settings.SHORT_LANGUAGE_CODE,
        )
        css = {
            'all': (
                'autocomplete/css/select2-bootstrap.css',
                'autocomplete/css/select2.css',
            )
        }

    def __init__(self, attrs=None, dependencies=(), expressions='title__icontains',
                 minimum_input_length=2, format_item=None, close_on_select=True,
                 template='autocomplete/autocomplete.html'):
        default_attrs = {
            'style': 'width: 250px',
            'placeholder': _('Search element'),
        }
        default_attrs.update(attrs or {})
        super().__init__(default_attrs)

        self.template = template
        self.dependencies = dependencies
        self.minimum_input_length = int(minimum_input_length)
        self.close_on_select = int(bool(close_on_select))

        # format_item
        if format_item is None:
            format_item = default_format_item
        self.format_item_module = format_item.__module__
        self.format_item_method = format_item.__qualname__

        # expressions
        if isinstance(expressions, (list, tuple)):
            expressions = ','.join(expressions)
        self.expressions = expressions

    def render(self, name, value, attrs=None):
        queryset = self.choices.queryset
        application = queryset.model._meta.app_label
        model_name = queryset.model._meta.model_name

        # Получаем имя без префикса формсета
        if len(name.split('-')) > 1:
            name_parts = name.split('-')
            real_name = '-'.join((name_parts[0], name_parts[-1]))
        else:
            real_name = name

        # Сохраняем данные в Redis
        cache.set('.'.join((application, model_name, real_name)), pickle.dumps({
            'query': queryset.query,
            'format_item_module': self.format_item_module,
            'format_item_method': self.format_item_method,
            'dependencies': self.dependencies,
        }), timeout=1800)

        # Аттрибуты
        attrs = self.build_attrs(attrs)

        attrs.update({
            'data-minimum_input_length': self.minimum_input_length,
            'data-expressions': self.expressions,
            'data-close_on_select': self.close_on_select,
            'data-depends': ','.join(item[1] for item in self.dependencies),
            'data-url': resolve_url('autocomplete:autocomplete_widget',
                application=application,
                model_name=model_name,
                name=real_name,
            )
        })

        # Добавляем класс
        classes = attrs.get('class', '')
        attrs['class'] = classes + ' autocomplete_widget'

        # Форматирование value
        if isinstance(value, (list, tuple)):
            value = ','.join(force_text(item) for item in value)

        # render
        return render_to_string(self.template, {
            'attrs': flatatt(attrs),
            'value': value or '',
            'name': name,
        })


class AutocompleteMultipleWidget(AutocompleteWidget):
    def render(self, name, value, attrs=None):
        default_attrs = {
            'data-multiple': 1,
        }
        default_attrs.update(attrs or {})
        return super().render(name, value, attrs=default_attrs)

    def value_from_datadict(self, data, files, name):
        """ Преобразует строку '1,2' в список (1,2) """
        value = super().value_from_datadict(data, files, name)
        if isinstance(value, (list, tuple)):
            value = value[0]
        return value.split(',') if value else None


class AutocompleteTextboxWidget(widgets.Widget):
    """
        Виджет для текстового поля с автокомплитом.
    """
    class Media:
        js = (
            'autocomplete/js/autocomplete_textbox.js',
        )
        css = {
            'all': (
                'autocomplete/css/autocomplete_textbox.css',
            )
        }

    def __init__(self, attrs=None, choices=(), template='autocomplete/autocomplete_textbox.html'):
        default_attrs = {
            'style': 'width: 250px',
            'placeholder': _('Input value'),
        }
        default_attrs.update(attrs or {})

        super().__init__(default_attrs)
        self.template = template
        self.choices = choices

    def render(self, name, value, attrs=None):
        # Аттрибуты
        attrs = self.build_attrs(attrs)

        if callable(self.choices):
            choices = self.choices()
        else:
            choices = self.choices

        return render_to_string(self.template, {
            'attrs': flatatt(attrs),
            'value': value or '',
            'name': name,
            'choices': choices,
        })
