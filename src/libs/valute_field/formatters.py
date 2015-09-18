import sys
import inspect
from decimal import Decimal, getcontext, ROUND_CEILING
from django.utils.translation import get_language
from .utils import split_price


class DollarFormatter:
    langs = ('en', )
    max_digits = 18
    decimal_places = 2
    separator = '.'
    decimal_mark = ','
    trail_zero_frac = True
    widget_attrs = {
        'prepend': '$'
    }

    @classmethod
    def canonical(cls, value, rounding=ROUND_CEILING):
        from .valute import Valute
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

        if cls.decimal_mark:
            dec_int = split_price(dec_int, cls.decimal_mark)

        if dec_frac:
            return cls.separator.join((dec_int, dec_frac))

        return dec_int

    @classmethod
    def utf(cls, value):
        str_value = cls.to_string(cls.canonical(value))
        return '${}'.format(str_value)

    @classmethod
    def alternate(cls, value):
        str_value = cls.to_string(cls.canonical(value))
        return '${}'.format(str_value)


class RoubleFormatter(DollarFormatter):
    langs = ('ru',)
    separator = '.'
    decimal_mark = ' '
    widget_attrs = {
        'append': 'руб.'
    }

    @classmethod
    def utf(cls, value):
        str_value = cls.to_string(cls.canonical(value))
        return '{}\u20bd'.format(str_value)

    @classmethod
    def alternate(cls, value):
        str_value = cls.to_string(cls.canonical(value))
        return '{} руб.'.format(str_value)


FORMATTERS = {}
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and hasattr(obj, 'langs'):
        for lang in getattr(obj, 'langs'):
            FORMATTERS[lang] = obj


def get_formatter():
    """ Получение текущего форматтера цены """
    current_lang = get_language()
    short_current_lang = current_lang.split('-')[0]
    return FORMATTERS.get(short_current_lang)