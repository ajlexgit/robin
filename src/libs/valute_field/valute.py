from decimal import Decimal, getcontext, ROUND_CEILING
from django.conf import settings


class DollarFormatter:
    max_digits = 18
    decimal_places = 2
    separator = ','
    trail_zero_frac = True
    utf_format = '${}'
    alternate_format = '${}'

    @classmethod
    def canonical(cls, value, rounding=ROUND_CEILING):
        context = getcontext().copy()
        context.prec = cls.max_digits
        context.rounding = rounding
        result = value.quantize(Decimal('.1') ** cls.decimal_places, context=context)
        return Valute(result)

    @classmethod
    def to_string(cls, value):
        str_value = '{0:f}'.format(value)
        dec_int, dec_frac = str_value.split('.')
        if cls.trail_zero_frac:
            trailed_frac = dec_frac.rstrip('0')
            if not trailed_frac:
                dec_frac = ''

        if dec_frac:
            return cls.separator.join((dec_int, dec_frac))

        return dec_int

    @classmethod
    def utf(cls, value):
        str_value = cls.to_string(cls.canonical(value))
        return cls.utf_format.format(str_value)

    @classmethod
    def alternate(cls, value):
        str_value = cls.to_string(cls.canonical(value))
        return cls.alternate_format.format(str_value)


class RoubleFormatter(DollarFormatter):
    separator = '.'
    utf_format = '{}\u20bd'
    alternate_format = '{} руб.'


FORMATTERS = {
    'en': DollarFormatter,
    'ru': RoubleFormatter,
}
FORMATTER = FORMATTERS[settings.SHORT_LANGUAGE_CODE]


class Valute(Decimal):
    def canonical(self, rounding=ROUND_CEILING):
        return FORMATTER.canonical(self, rounding=rounding)

    @property
    def utf(self):
        return FORMATTER.utf(self)

    @property
    def alternate(self):
        return FORMATTER.alternate(self)

    def __repr__(self):
        return "Valute('%s')" % str(self)

    def __neg__(self, *args, **kwargs):
        return self.__class__(super().__neg__(*args, **kwargs))

    def __abs__(self, *args, **kwargs):
        return self.__class__(super().__abs__(*args, **kwargs))

    def __add__(self, *args, **kwargs):
        return self.__class__(super().__add__(*args, **kwargs))

    __radd__ = __add__

    def __sub__(self, *args, **kwargs):
        return self.__class__(super().__sub__(*args, **kwargs))

    def __rsub__(self, *args, **kwargs):
        return self.__class__(super().__rsub__(*args, **kwargs))

    def __mul__(self, *args, **kwargs):
        return self.__class__(super().__mul__(*args, **kwargs))

    def __truediv__(self, *args, **kwargs):
        return self.__class__(super().__truediv__(*args, **kwargs))

    def __rtruediv__(self, *args, **kwargs):
        return self.__class__(super().__rtruediv__(*args, **kwargs))

    def __divmod__(self, *args, **kwargs):
        return self.__class__(super().__divmod__(*args, **kwargs))

    def __rdivmod__(self, *args, **kwargs):
        return self.__class__(super().__rdivmod__(*args, **kwargs))

    def __mod__(self, *args, **kwargs):
        return self.__class__(super().__mod__(*args, **kwargs))

    def __rmod__(self, *args, **kwargs):
        return self.__class__(super().__rmod__(*args, **kwargs))

    def __floordiv__(self, *args, **kwargs):
        return self.__class__(super().__floordiv__(*args, **kwargs))

    def __rfloordiv__(self, *args, **kwargs):
        return self.__class__(super().__rfloordiv__(*args, **kwargs))
