"""
    Поле выбора файла.

    1) Удаляет файл при удалении модели
    2) Удаляет старый файл при загрузке нового
"""

from .fields import FileField, ImageField
from .widgets import FileWidget
