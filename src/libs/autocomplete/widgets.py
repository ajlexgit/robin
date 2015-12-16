import pickle
from django.conf import settings
from django.forms import widgets
from django.core.cache import caches
from django.forms.models import ModelChoiceIterator
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
    _choices = ()
    app_label = ''
    model_name = ''

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

        # модуль и имя функции, форматирующей каждый элемент
        # выпадающего списка автокомплита
        if format_item is None:
            format_item = default_format_item
        self.format_item_module = format_item.__module__
        self.format_item_method = format_item.__qualname__

        # ключи фильтров выборки
        if isinstance(expressions, (list, tuple)):
            expressions = ','.join(expressions)
        self.expressions = expressions

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        """ Определение модели, по которой производится выборка """
        self._choices = value
        if isinstance(value, ModelChoiceIterator):
            self.app_label = value.queryset.model._meta.app_label
            self.model_name = value.queryset.model._meta.model_name
        else:
            raise TypeError('choices for AutocompleteWidget must be an instance of ModelChoiceIterator')

    def get_short_name(self, name):
        """
            Получение имени поля без индекса inline-формы,
            которые добавляются от inline-форм.

            Пример:
                model-0-field -> model-field
        """
        if '-' in name:
            name_parts = name.split('-')
            return '-'.join((name_parts[0], name_parts[-1]))

        return name

    def _cache_data(self, cache_keys=()):
        """ Сохранение некоторых данных в кэш """
        cache_key = '.'.join(cache_keys)
        cache.set(cache_key, pickle.dumps({
            'query': self.choices.queryset.query,
            'format_item_module': self.format_item_module,
            'format_item_method': self.format_item_method,
            'dependencies': self.dependencies,
        }), timeout=1800)

    def get_url(self, name):
        """ Построение урла для запроса данных """
        return resolve_url('autocomplete:autocomplete_widget',
            application=self.app_label,
            model_name=self.model_name,
            name=name,
        )

    def render(self, name, value, attrs=None):
        short_name = self.get_short_name(name)
        self._cache_data((self.app_label, self.model_name, short_name))

        # Аттрибуты
        final_attrs = self.build_attrs(attrs, name=name, **{
            'data-minimum_input_length': self.minimum_input_length,
            'data-expressions': self.expressions,
            'data-close_on_select': self.close_on_select,
            'data-depends': ','.join(item[1] for item in self.dependencies),
            'data-url': self.get_url(short_name),
        })

        # Добавляем класс
        classes = final_attrs.get('class', '')
        final_attrs['class'] = classes + ' autocomplete_widget'

        # Форматирование множественного значения
        if isinstance(value, (list, tuple)):
            value = ','.join(force_text(item) for item in value)

        # render
        return render_to_string(self.template, {
            'attrs': flatatt(final_attrs),
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

