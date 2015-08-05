from decimal import Decimal, getcontext
from .utils import color_from_string


class Color:
    __slots__ = ('_color', '_opacity', '_int_color')

    def __new__(cls, color, opacity='1'):
        self = object.__new__(cls)

        if ':' in color:
            color, opacity = color.split(':')

        self.color = color
        self.opacity = opacity
        return self

    @property
    def opacity(self):
        opacity = str(self._opacity).rstrip('0').rstrip('.')
        return opacity if opacity else '0'

    @opacity.setter
    def opacity(self, value):
        cleaned_opacity = Decimal(value)
        if cleaned_opacity < 0:
            cleaned_opacity = Decimal()
        elif cleaned_opacity > 1:
            cleaned_opacity = Decimal(1)
        context = getcontext().copy()
        context.prec = 3
        self._opacity = cleaned_opacity.quantize(Decimal('0.01'), context=context)

    @property
    def color(self):
        return '#%s' % self._color

    @color.setter
    def color(self, value):
        cleaned_color = color_from_string(value)
        if not cleaned_color:
            raise ValueError('Wrong color "%s"' % value)
        else:
            self._color = cleaned_color
            self._int_color = tuple(
                int(cleaned_color[i:i+2], 16)
                for i in range(0, len(cleaned_color), 2)
            )

    @property
    def rgb(self):
        return 'rgb({0}, {1}, {2})'.format(*self._int_color)

    @property
    def rgba(self):
        return 'rgba({1}, {2}, {3}, {0})'.format(self.opacity, *self._int_color)

    def to_string(self):
        return '{}:{}'.format(self._color, self._opacity)

    def __repr__(self):
        if self._opacity == 1:
            return self.color
        else:
            return self.rgba
