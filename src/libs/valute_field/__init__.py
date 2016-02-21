"""
    Поле для хранения цены в формате decimal.
    Имеет дополнительные методы uft и alternative для вывода суммы со знаком валюты.

    Пример:
        price = ValuteField(_('цена'))

        ru:
            $ v = Valute('1234.00')
            $ print(v)
            1 234 ₽

            $ print(v.utf)
            1 234 ₽

            $ print(v.alternative)
            1 234 руб.

            $ print(v.simple)
            1 234.00

            $ print(v.trailed)
            1 234

"""

from .valute import Valute
from .fields import ValuteField
from .forms import ValuteFormField

__all__ = ['Valute', 'ValuteField']