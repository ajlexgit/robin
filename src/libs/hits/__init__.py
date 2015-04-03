"""
    Модуль счетчика по дням для экземпляров моделей.
    
    Примеры:
        entry = Post.objects.get(pk=1)
        
        # Получить сумму значений счетчика за всё время
        total_hits = Hits.get(entry, type='my action')
        
        # Увеличить счетчик (для текущего дня) на 1
        Hits.increment(entry, type='other action')
        
        # Получить значение счетчика за вчерашний день
        since = datetime.now() - timedelta(1)
        to = since
        yesterday_hits = Hits.get(entry, type='my action', since=since, to=to)
        
        # Удалить все значения счетчика
        Hits.clear(entry, type='my action')
"""