from decimal import Decimal, ROUND_CEILING
from .formatters import get_formatter


class Valute(Decimal):
    def canonical(self, rounding=ROUND_CEILING):
        return get_formatter().canonical(self, rounding=rounding)

    @property
    def utf(self):
        return get_formatter().utf(self)

    @property
    def alternate(self):
        return get_formatter().alternate(self)

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
