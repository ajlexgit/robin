from .base import request


def get_all(page=0, limit=100):
    """ Получение всех рассылок """
    return request('campaigns', params={
        'page': page+1,
        'limit': limit,
    }, version=1)['Results']


def get(campaign_id):
    """ Получение информации о рассылке """
    return request('campaigns/%d' % campaign_id, version=1)


def create(subject, groups, from_email, from_name, language='en'):
    """
        Создание рассылки.

        Метки:
            {$email} - user email
            {$name} - first name
            {$last_name} - last name
            {$company} - user company
    """
    return request('campaigns', method='POST', data={
        'type': 'regular',
        'subject': subject,
        'from': from_email,
        'from_name': from_name,
        'groups': groups,
        'language': language,
    })


def content(campaign_id, html, plain):
    """
        Установка содержимого рассылки.
        ОБЯЗАТЕЛЬНО наличие ссылки на отписку:
            <a href="{$unsubscribe}">Unsubscribe</a>

        Метки:
            {$url} - URL to your HTML newsletter
            {$email} - user email
            {$name} - first name
            {$last_name} - last name
            {$company} - user company
            {$unsubscribe} - unsubscribe link
    """
    return request('campaigns/%d/content' % campaign_id, method='PUT', data={
        'html': html,
        'plain': plain,
        'auto_inline': 'true',
    })


def run(campaign_id, action='send'):
    """
        Запуск/отмена рассылки.

        Параметр action: send/cancel
    """
    return request('campaigns/%d/actions/%s' % (campaign_id, action), method='POST')
