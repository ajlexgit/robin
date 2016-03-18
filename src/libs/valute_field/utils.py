import re
from django.conf import settings
from django.utils.translation import get_language
from django.core.exceptions import ImproperlyConfigured

VALUTE_FORMATS = getattr(settings, 'VALUTE_FORMATS', {})

re_price = re.compile(r'^(-?\d+)(\d{3})')


def get_formatter(language=None):
    language = language or get_language() or settings.LANGUAGE_CODE
    for langs, valute_format in VALUTE_FORMATS.items():
        if language in langs:
            return valute_format
    else:
         raise ImproperlyConfigured("Valute format not found for language '%s'" % language)


def split_price(value, join=' '):
    """ Разделение цены по разрядам """
    new = re_price.sub('\\1{}\\2'.format(join), value)
    if value == new:
        return new
    else:
        return split_price(new, join)
