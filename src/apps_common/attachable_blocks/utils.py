from inspect import isclass
from django.apps import apps


def get_block_type(cls):
    model = cls if isclass(cls) else cls.__class__

    block_type = getattr(model, '_cached_block_key', '')
    if not block_type:
        app_name = model.__module__.rsplit('.')[0]
        model_name = model.__qualname__
        block_type = '.'.join((app_name, model_name)).lower()
        model._cached_block_key = block_type

    return block_type


def get_model(fullname):
    return apps.get_model(*fullname.rsplit('.', 1))