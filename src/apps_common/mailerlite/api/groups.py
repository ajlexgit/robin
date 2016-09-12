from .base import request


def get_all(limit=100, offset=0, filters=None):
    """ Получение всех списков подписчиков """
    return request('groups', params={
        'limit': limit,
        'offset': offset,
        'filters': filters,
    })


def get(group_id):
    """ Получение информации о списке подписчиков """
    return request('groups/%d' % group_id)


def create(name):
    """ Создание списка подписчиков """
    return request('groups', method='POST', data={
        'name': name,
    })


def update(group_id, name):
    """ Обновление списка подписчиков """
    return request('groups/%d' % group_id, method='PUT', data={
        'name': name,
    })


def subscribers(group_id, limit=100, offset=0, filters=None, status=None):
    """
        Получение подписчиков из списка.
        Параметр status: active/unsubscribed/bounced/junk/unconfirmed
    """
    if status:
        return request('groups/%d/subscribers/%s' % (group_id, status), params={
            'limit': limit,
            'offset': offset,
            'filters': filters,
        })
    else:
        return request('groups/%d/subscribers' % group_id, params={
            'limit': limit,
            'offset': offset,
            'filters': filters,
        })


def delete(group_id):
    """ Удаление списка """
    return request('groups/%d' % group_id, method='DELETE')
