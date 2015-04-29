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
        elif code in self.error_messages:
            self.add_error(fieldname, ValidationError(
                self.error_messages[code],
                code=code,
                params=params
            ))
        else:
            raise ValueError('Unknown code %r' % code)

    @property
    def error_list(self):
        """ Список всех ошибок """
        return tuple((key, self.errors.get(key)) for key in self.fields if key in self.errors)
