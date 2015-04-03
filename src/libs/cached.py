from hashlib import md5
from random import randint
from django.core.cache import caches


def make_key(func, params=(), additions=()):
    """ Возвращает ключ кэша функции с указанными параметрами.

    Параметры:
        func      - функция
        params    - последовательность значений, которые составят ключ кэша
        additions - дополнительные значения для составления ключа кэша
    """
    final_params = [func.__module__, func.__qualname__]
    for param in params:
        param = str(param)
        # Требуем, чтобы ключ состоял только из latin-1
        try:
            param.encode('latin-1')
        except UnicodeEncodeError:
            param = md5(param.encode()).hexdigest()
        final_params.append(param)
    final_params.extend(additions)
    return '.'.join(final_params)


def cached(cache_time, key_params=(), key_addition=(), backend='default'):
    """ Декоратор кэширования функций и методов, 
    использующий для составления ключа значения параметров функции.
    
    Поддерживает указание атрибутов параметров, например "request.city.id".
    Данная нотация может быть использована и для свойств и для индексов (dectionary.index).

    Параметры:
        cache_time      - время кэширования в секундах
        key_params      - список/кортеж имен параметров функции, которые
                          будут использованы для составления ключа кэша
        key_addition    - список/кортеж дополнительных значений, которые будут использованы 
                          для составления ключа кэша
        backend         - идентификатор используемого бэкенда кэширования
    
    Пример использования:
        @cached(600, ['title', 'address.street', 'addition.key'], [settings.CACHE_VERSION])
        def MyFunc(title, address, addition={'key': 1})
            ...
            return ...
    
    """
    cache = caches[backend]
    
    def decorator(func):
        varnames = func.__code__.co_varnames
        _defaults = func.__defaults__ or ()
        defaults = dict(zip(varnames[-len(_defaults):], _defaults))
        
        def wrapper(*args, **kwargs):
            func_args = defaults.copy()
            func_args.update(zip(varnames[:len(args)], args))
            func_args.update(kwargs)

            # Получение значений параметров функции
            real_params = []
            for name in (key_params or varnames):
                properties = name.split('.')
                value = func_args.get(properties.pop(0), None)
                for prop in properties:
                    if value is None:
                        break

                    try:
                        value = getattr(value, prop, None)
                    except AttributeError:
                        value = value.get(prop, None)

                    if callable(value):
                        value = value()

                real_params.append(value)

            key = make_key(func, real_params, key_addition)
            if key in cache:
                return cache.get(key)
            else:
                result = func(*args, **kwargs)
                if not result is None:
                    # Размазываем по времени (±10%), чтобы избежать
                    # обновления множества кэшированных данных одновременно.
                    amplitude = round(cache_time * 0.1)
                    final_time = max(20, cache_time + randint(-amplitude, amplitude))
                    cache.set(key, result, final_time)
                
                return result
        return wrapper
    return decorator