from .base import request


def get_all(limit=100, offset=0, filters=None):
    """ Получение всех списков подписчиков """
    return request('groups', params={
        'limit': limit,
        'offset': offset,
        'filters': filters or {},
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


def subscribers(group_id, limit=100, offset=0, filters=None, status='active'):
    """
        Получение подписчиков из списка.
        Параметр status: active/unsubscribed/bounced/junk/unconfirmed
    """
    return request('groups/%d/subscribers' % group_id, params={
        'limit': limit,
        'offset': offset,
        'filters': filters or {},
        'type': status,
    })


def delete(group_id):
    """ Удаление списка """
    return request('groups/%d' % group_id, method='DELETE')
