from django.core.urlresolvers import reverse, NoReverseMatch

ADMIN_NAMESPACE = 'admin'


def get_add_url(instance_or_model, popup=False):
    """ Возвращает ссылку на добавление сущности в админке """
    meta = getattr(instance_or_model, '_meta')
    try:
        url = reverse(
            '{}:{}_{}_add'.format(ADMIN_NAMESPACE, meta.app_label, meta.model_name)
        )
    except NoReverseMatch:
        return None
    else:
        if popup:
            url += '?_to_field=id&_popup=1'
        return url


def get_change_url(instance, popup=False):
    """ Возвращает ссылку на редактирование сущности в админке """
    meta = getattr(instance, '_meta')
    try:
        url = reverse(
            '{}:{}_{}_change'.format(ADMIN_NAMESPACE, meta.app_label, meta.model_name),
            args=(instance.pk,)
        )
    except NoReverseMatch:
        return None
    else:
        if popup:
            url += '?_to_field=id&_popup=1'
        return url


def get_delete_url(instance, popup=False):
    """ Возвращает ссылку на удаление сущности в админке """
    meta = getattr(instance, '_meta')
    try:
        url = reverse(
            '{}:{}_{}_delete'.format(ADMIN_NAMESPACE, meta.app_label, meta.model_name),
            args=(instance.pk,)
        )
    except NoReverseMatch:
        return None
    else:
        if popup:
            url += '?_to_field=id&_popup=1'
        return url


def add_popup_data(instance_or_model):
    """
        Возвращает URL, "onclick" и "id" для формирования ссылки на добавление сущности
        через Popup-окно.

        Пример:
            popup_data = admin_utils.add_popup_data(obj)
            return '<a href="{href}" id="{id}" onclick="{onclick}">{text}</a>'.format(
                text = str(obj),
                **popup_data
            )
    """
    meta = getattr(instance_or_model, '_meta')
    return {
        'href': get_add_url(instance_or_model, popup=True),
        'onclick': 'showAddAnotherPopup(this); return false;',
        'id': 'add_id_%s' % meta.model_name,
    }


def change_popup_data(instance):
    """
        Возвращает URL, "onclick" и "id" для формирования ссылки на изменение сущности
        через Popup-окно.

        Пример:
            popup_data = admin_utils.change_popup_data(obj)
            return '<a href="{href}" id="{id}" onclick="{onclick}">{text}</a>'.format(
                text = str(obj),
                **popup_data
            )
    """
    meta = getattr(instance, '_meta')
    return {
        'href': get_change_url(instance, popup=True),
        'onclick': 'showRelatedObjectPopup(this); return false;',
        'id': 'change_id_%s' % meta.model_name,
    }


