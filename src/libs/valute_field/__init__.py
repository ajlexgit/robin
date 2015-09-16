"""
    Поле для хранения цены в формате decimal.
    Имеет дополнительные методы uft и alternate для вывода суммы со знаком валюты.

    Пример:
        price = ValuteField(_('цена'))

        ru:
            >>> obj.price = '3.56'
            >>> print(obj.price.utf)
            3.56₽
            >>> print(obj.price.alternate)
            3.56 руб.
"""

from .fields import ValuteField
from .valute import Valute

__all__ = ['Valute', 'ValuteField']