from decimal import Decimal, getcontext, ROUND_CEILING
from django.utils.functional import cached_property
from .utils import split_price, get_formatter


class Valute:
    def __init__(self, value='0', rounding=ROUND_CEILING):
        # настройки форматирования
        self._formatter = get_formatter()

        # форматирование числа
        context = getcontext().copy()
        context.prec = 18
        context.rounding = rounding
        value = Decimal(value)
        self._value = value.quantize(Decimal('.1') ** self._formatter['decimal_places'], context=context)

        # целая и дробная части
        self._int, self._frac = str(self._value).rsplit('.', 1)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self)

    def _join(self, int_part, frac_part):
        """ Объединение частей цены разделителем """
        if not frac_part:
            return int_part
        else:
            return self._formatter['decimal_mark'].join((int_part, frac_part))

    def _thousands(self, value):
        """ Разделение на тысячные разряды """
        if self._formatter['thousands']:
            value = split_price(value, join=self._formatter['thousands'])
        return value

    # ===========
    # Форматы
    # ===========

    def __str__(self):
        return self.utf

    def as_decimal(self):
        return self._value

    def as_string(self):
        _int = self._int
        _frac = self._frac
        return self._join(_int, _frac)

    @cached_property
    def simple(self):
        """
            Без символа валюты,
            без удаления финальных нулей,
            с разделением на разряды

            Пример: 12 340.00
        """
        _int = self._thousands(self._int)
        _frac = self._frac
        return self._join(_int, _frac)

    @cached_property
    def trailed(self):
        """
            Без символа валюты,
            c удалением финальных нулей,
            с разделением на разряды

            Пример: 12 340
        """
        _int = self._thousands(self._int)
        _frac = self._frac if self._frac.strip('0') else ''
        return self._join(_int, _frac)

    @cached_property
    def utf(self):
        """
            С символом валюты,
            c удалением финальных нулей (конфиг),
            с разделением на разряды

            Пример: 12,340.00 Р
        """
        if self._formatter['trail']:
            value = self.trailed
        else:
            value = self.simple

        return self._formatter['utf_format'].format(value)

    @cached_property
    def alternative(self):
        """
            С символом валюты (без UTF),
            c удалением финальных нулей (конфиг),
            с разделением на разряды

            Пример: 12,340.00 руб
        """
        if self._formatter['trail']:
            value = self.trailed
        else:
            value = self.simple

        return self._formatter['alternative_format'].format(value)

    # ===========
    # Операторы
    # ===========

    def __bool__(self):
        return bool(self._value)

    def __eq__(self, other):
        if isinstance(other, Valute):
            return self._value.__eq__(other._value)
        return self._value.__eq__(other)

    def __ne__(self, other):
        if isinstance(other, Valute):
            return self._value.__ne__(other._value)
        return self._value.__ne__(other)

    def __lt__(self, other):
        if isinstance(other, Valute):
            return self._value.__lt__(other._value)
        return self._value.__lt__(other)

    def __le__(self, other):
        if isinstance(other, Valute):
            return self._value.__le__(other._value)
        return self._value.__le__(other)

    def __gt__(self, other):
        if isinstance(other, Valute):
            return self._value.__gt__(other._value)
        return self._value.__gt__(other)

    def __ge__(self, other):
        if isinstance(other, Valute):
            return self._value.__ge__(other._value)
        return self._value.__ge__(other)

    def __neg__(self):
        return self.__class__(self._value.__neg__())

    def __abs__(self, round=True):
        return self.__class__(self._value.__abs__(round))

    def __add__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__add__(other._value))
        return self.__class__(self._value.__add__(other))

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__sub__(other._value))
        return self.__class__(self._value.__sub__(other))

    def __rsub__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__rsub__(other._value))
        return self.__class__(self._value.__rsub__(other))

    def __mul__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__mul__(other._value))
        return self.__class__(self._value.__mul__(other))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__truediv__(other._value))
        return self.__class__(self._value.__truediv__(other))

    def __rtruediv__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__rtruediv__(other._value))
        return self.__class__(self._value.__rtruediv__(other))

    def __divmod__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__divmod__(other._value))
        return self.__class__(self._value.__divmod__(other))

    def __rdivmod__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__rdivmod__(other._value))
        return self.__class__(self._value.__rdivmod__(other))

    def __mod__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__mod__(other._value))
        return self.__class__(self._value.__mod__(other))

    def __rmod__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__rmod__(other._value))
        return self.__class__(self._value.__rmod__(other))

    def __floordiv__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__floordiv__(other._value))
        return self.__class__(self._value.__floordiv__(other))

    def __rfloordiv__(self, other):
        if isinstance(other, Valute):
            return self.__class__(self._value.__rfloordiv__(other._value))
        return self.__class__(self._value.__rfloordiv__(other))
