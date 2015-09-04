def associative(data):
    """
        Форматирует словарь данных запроса в ассоциативный массив:

        Пример:
            >>> associative({'plain': 1, 'list': [1,2], 'dict': {'a':1, 'b':2}})
            >>> {'plain': 1, 'list[0]': 1, 'list[1]': 2, 'dict[a]': 1, 'dict[b]': 2}
    """
    result = {}

    def _process(inner_data, prefix):
        if isinstance(inner_data, (tuple, list)):
            for index, item in enumerate(inner_data):
                _process(item, '{}[{}]'.format(prefix, index))
        elif isinstance(inner_data, dict):
            for index, item in inner_data.items():
                _process(item, '{}[{}]'.format(prefix, index))
        else:
            result[prefix] = inner_data

    for key, value in data.items():
        if isinstance(value, (list, tuple, dict)):
            _process(value, key)
        else:
            result[key] = value
    return result