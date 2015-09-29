from decimal import Decimal, localcontext, ROUND_HALF_UP, InvalidOperation


def format_decimal(value):
    try:
        value = Decimal(value)
    except (InvalidOperation, TypeError):
        return None
    else:
        with localcontext() as ctx:
            ctx.prec = 14
            ctx.rounding = ROUND_HALF_UP
            return value + 0


class Coords:
    """
        Класс, описывающий пару координат.
        Используется в yandex_maps и google_maps.
    """
    __slots__ = ('_lat', '_lng')

    def __init__(self, lng=None, lat=None):
        self.lng = lng
        self.lat = lat

    @property
    def lng(self):
        return self._lng

    @property
    def lat(self):
        return self._lat

    @lng.setter
    def lng(self, value):
        self._lng = format_decimal(value)

    @lat.setter
    def lat(self, value):
        self._lat = format_decimal(value)

    def __bool__(self):
        return self.lng is not None and self.lat is not None

    def __iter__(self):
        if self:
            return iter((self.lng, self.lat))

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        if self:
            return '{0}, {1}'.format(self.lng, self.lat)
        else:
            return ''
