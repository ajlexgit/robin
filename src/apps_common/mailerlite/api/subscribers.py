from .base import request


def get(id_or_email):
    """ Получение информации о подписчике """
    return request('subscribers/%s' % id_or_email)


def search(query='', limit=100, offset=0, minimized=True):
    """ Поиск по подписчикам """
    return request('subscribers/search', params={
        'query': query,
        'limit': limit,
        'offset': offset,
        'minimized': 'true' if minimized else 'false',
    })


def fetch_groups(id_or_email):
    """ Получение групп, в которых состоит подписчик """
    return request('subscribers/%s/groups' % id_or_email)


def fetch_activity(id_or_email):
    """ Получение статистики активности подписчика """
    return request('subscribers/%s/activity' % id_or_email)


def prepare_subscriber(email, first_name='', last_name='', company='', status='active'):
    """ Создание объекта подписчика для передачи в create или bulk_create """
    fields = {
        'name': first_name,
        'last_name': last_name,
        'company': company,
    }
    return {
        'email': email,
        'fields': {key: value for key, value in fields.items() if value},
        'type': status,
    }


def create(group_id, *args, resubscribe=False, **kwargs):
    """ Создание подписчика """
    subscriber = prepare_subscriber(*args, **kwargs)
    subscriber['resubscribe'] = 'true' if resubscribe else 'false',
    return request('groups/%d/subscribers' % group_id, method='POST', data=subscriber)


def bulk_create(group_id, subscribers, resubscribe=False):
    """
        Создание множества подписчиков
    """
    return request('groups/%d/subscribers/import' % group_id, method='POST', data={
        'subscribers': subscribers,
        'resubscribe': 'true' if resubscribe else 'false',
    })


def delete(group_id, id_or_email):
    """ Удаление подписчика из списка """
    return request('groups/%d/subscribers/%s' % (group_id, id_or_email), method='DELETE')
