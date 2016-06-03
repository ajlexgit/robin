from django.shortcuts import resolve_url
from django.contrib.admin.filters import ListFilter
from django.core.exceptions import ImproperlyConfigured


class AutocompleteListFilter(ListFilter):
    title = None
    parameter_name = None
    empty_values = (None, '', [], ())
    template = 'autocomplete/filter.html'

    width = 170                         # ширина виджета
    model = None                        # модель для выборки
    multiple = False                    # возможность выбора нескольких значений
    expression = 'title__icontains'     # ключ для фильтрации
    minimum_input_length = 0            # минимальное кол-во введенных символов

    def __init__(self, request, params, model, model_admin):
        if self.model is None:
            raise ImproperlyConfigured(
                "The filter '%s' does not specify  a 'model'." % self.__class__.__name__)

        if self.title is None:
            self.title = self.model._meta.verbose_name

        if self.parameter_name is None:
            self.parameter_name = self.model_name.lower()

        super().__init__(request, params, model, model_admin)

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    @property
    def app_label(self):
        return self.model._meta.app_label

    @property
    def model_name(self):
        return self.model._meta.model_name

    @property
    def url(self):
        return resolve_url('autocomplete:autocomplete_filter',
            application=self.app_label,
            model_name=self.model_name
        )

    def has_output(self):
        return True

    def choices(self, cl):
        return ()

    def value(self):
        value = self.used_parameters.get(self.parameter_name, None)
        if self.multiple and ',' in value:
            return value.split(',')
        return value

    def expected_parameters(self):
        return [self.parameter_name]

    def queryset(self, request, queryset, value=None):
        value = self.value()
        if value in self.empty_values:
            return queryset
        else:
            return self.filter(queryset, value)

    def filter(self, queryset, value):
        return queryset