"""
    Миксина для форм, добавляющая форматированные списки ошибок
    form.error_list и form_error_list_full
"""

from django.forms.utils import ErrorList
from django.utils.html import format_html
from django.core.exceptions import ValidationError


class PlainErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''

        return format_html(
            '<span class="error">{}</span>'.format(
                ', '.join(str(e) for e in self)
            )
        )

    @property
    def classes(self):
        """ CSS-классы с кодами ошибок """
        if not self:
            return ''
        classes = set('error-%s' % e.code for e in self.as_data() if e.code)
        return 'errors %s' % ' '.join(classes)


class PlainErrorFormMixin:
    """
        Форматирует ошибки полей формы в виде:
            <span class="error">...</span>
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = PlainErrorList

    def add_field_error(self, fieldname, code, params=None):
        """
            Возбуждает ошибку валидации в поле fieldname с кодом code
        """
        field = self.fields[fieldname]
        if code in field.error_messages:
            self.add_error(fieldname, ValidationError(
                field.error_messages[code],
                code=code,
                params=params
            ))
        elif hasattr(self, 'error_messages') and code in self.error_messages:
            self.add_error(fieldname, ValidationError(
                self.error_messages[code],
                code=code,
                params=params
            ))
        else:
            raise ValueError('Unknown code %r' % code)

    @property
    def error_list(self):
        """ Список ошибок полей """
        return tuple((key, self.errors.get(key)) for key in self.fields if key in self.errors)

    @property
    def error_list_full(self):
        """ Список всех ошибок """
        return tuple(self.errors.items())

    @property
    def error_dict(self):
        """ Список словарей ошибок полей """
        result = []
        for key in self.fields:
            if key in self.errors:
                err_list = self.errors.get(key)
                result.append({
                    'field': key,
                    'errors': err_list,
                    'classes': err_list.classes
                })
        return tuple(result)

    @property
    def error_dict_full(self):
        """ Список словарей всех ошибок """
        return tuple({
            'field': key,
            'errors': err_list,
            'classes': err_list.classes
        } for key, err_list in self.errors.items())
