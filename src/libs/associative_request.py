from collections import Iterable


def _process(result, key, data):
    if isinstance(data, str):
        result[key] = data
    elif isinstance(data, dict):
        for index, inner_data in data.items():
            _process(result, '{}[{}]'.format(key, index), inner_data)
    elif isinstance(data, Iterable):
        for index, inner_data in enumerate(data):
            _process(result, '{}[{}]'.format(key, index), inner_data)
    else:
        result[key] = data


def associative(data):
    """
        Форматирует словарь данных запроса в ассоциативный массив:

        Пример:
            > associative({'plain': 1, 'list': [1,2], 'dict': {'a':1, 'b':2}})
            {'plain': 1, 'list[0]': 1, 'list[1]': 2, 'dict[a]': 1, 'dict[b]': 2}
    """
    if not data:
        return {}

    result = {}
    for key, value in data.items():
        _process(result, key, value)
    return result
