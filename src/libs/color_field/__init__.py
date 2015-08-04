"""
    Поле для хранения цвета в формате #FFFFFF (в БД - FFFFFF).

    Пример:
        color = ColorField('цвет', blank=True, default='#FF0000')
"""

from .color import Color
from .fields import ColorField, ColorOpacityField
