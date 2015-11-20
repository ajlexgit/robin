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


