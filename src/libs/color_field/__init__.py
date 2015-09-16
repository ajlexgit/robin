"""
    Поля для хранения цвета и цвета с прозрачностью.

    Пример:
        color = ColorField('цвет', blank=True, default='#FF0000')
        color2 = ColorOpacityField('цвет', blank=True, default='#FF0000:0.75')
"""

from .color import Color
from .fields import ColorField, ColorOpacityField

__all__ = ['Color', 'ColorField', 'ColorOpacityField']