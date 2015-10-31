"""
    Поле для хранения цены в формате decimal.
    Имеет дополнительные методы uft и alternate для вывода суммы со знаком валюты.

    Пример:
        price = ValuteField(_('цена'))

        ru:
            $ v = Valute('1234.56')
            $ print(v)
            1234.56

            $ print(v.plain)
            1 234.56

            $ print(v.utf)
            1 234.56₽

            $ print(v.alternate)
            1 234.56 руб.
"""

from .valute import Valute
from .fields import ValuteField
from .forms import ValuteFormField

__all__ = ['Valute', 'ValuteField']