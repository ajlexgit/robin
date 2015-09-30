from numbers import Number
from decimal import Decimal, localcontext, ROUND_HALF_UP, InvalidOperation

__all__ = ['Coords']


class Coords:
    """
        Класс, описывающий пару координат.
        Используется в yandex_maps и google_maps.
    """
    __slots__ = ('_lat', '_lng')

    def __new__(cls, lng=None, lat=None):
        self = object.__new__(cls)
        self._lng = self._format_number(lng)
        self._lat = self._format_number(lat)
        return self

    @classmethod
    def _format_number(cls, number):
        if isinstance(number, (Number, str)):
            try:
                value = Decimal(number)
            except InvalidOperation:
                raise ValueError('Invalid coordinate format: %r' % number)
            else:
                with localcontext() as ctx:
                    ctx.prec = 13
                    ctx.rounding = ROUND_HALF_UP
                    return value + 0
        elif isinstance(number, Decimal):
            return number
        else:
            raise TypeError('Invalid coordinates type: %r' % number)

    @property
    def lat(self):
        return self._lat

    @property
    def lng(self):
        return self._lng

    def __iter__(self):
        return iter((self.lng, self.lat))

    def __repr__(self):
        return '{0}, {1}'.format(self.lng, self.lat)
