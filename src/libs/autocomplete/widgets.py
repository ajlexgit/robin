import pickle
from django.conf import settings
from django.forms import widgets
from django.core.cache import caches
from django.forms.utils import flatatt
from django.shortcuts import resolve_url
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

CACHE_BACKEND = getattr(settings,  'AUTOCOMPLETE_CACHE_BACKEND', 'default')
cache = caches[CACHE_BACKEND]


class AutocompleteWidgetMixin:
    template = 'autocomplete/autocomplete.html'
    item2dict_module = None
    item2dict_method = None
    dependencies = ()

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

    def render(self, name, value, attrs=None, choices=()):
        attrs = attrs or {}
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
            'item2dict_module': self.item2dict_module,
            'item2dict_method': self.item2dict_method,
            'dependencies': self.dependencies,
        }), timeout=1800)

        attrs.update({
            'data-depends': ','.join(item[1] for item in self.dependencies),
            'data-url': resolve_url('autocomplete:autocomplete_widget',
                application=application,
                model_name=model_name,
                name=real_name,
            )
        })

        final_attrs = self.build_attrs(attrs)

        # Добавляем класс
        classes = final_attrs.get('class', '')
        final_attrs['class'] = classes + ' autocomplete_widget'

        # render
        output = [render_to_string(self.template, {
            'attrs': flatatt(final_attrs),
            'value': value or '',
            'name': name,
        })]

        return mark_safe(''.join(output))


class AutocompleteWidget(AutocompleteWidgetMixin, widgets.Select):
    pass


class AutocompleteMultipleWidget(AutocompleteWidgetMixin, widgets.SelectMultiple):
    def value_from_datadict(self, data, files, name):
        """ Преобразует строку '1,2' в список (1,2) """
        value = super().value_from_datadict(data, files, name)
        if isinstance(value, (list, tuple)):
            value = value[0]
        return value.split(",") if value else None
