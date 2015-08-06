from django.apps import apps


def get_model(fullname):
    """
        Получение модели по полному имени, получаемому так:
            '%s.%s' % (cls.__module__, cls.__qualname__)

    """
    return apps.get_model(*fullname.rsplit('.', 1))