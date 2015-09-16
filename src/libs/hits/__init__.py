"""
    Модуль счетчика по дням для экземпляров моделей.

    Примеры:
        entry = Post.objects.get(pk=1)

        # Увеличить счетчик типа shows (для текущего дня) на 1
        Hits.increment(entry, name='shows')

        # Получить сумму значений счетчика shows за всё время
        total_hits = Hits.get(entry, name='shows')

        # Получить значение счетчика click за вчерашний день
        yesterday = datetime.now() - timedelta(1)
        yesterday_hits = Hits.get(entry, name='click', since=yesterday, to=yesterday)

        # Удалить все значения счетчика click
        Hits.clear(entry, name='click')
"""

from .models import Hits

__all__ = ['Hits']