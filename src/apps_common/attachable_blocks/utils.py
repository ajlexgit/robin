from inspect import isclass
from importlib import import_module
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


def get_block_view(block):
    _cached = getattr(block, '_BLOCK_VIEW', '')
    if _cached:
        return _cached

    path = getattr(block, 'BLOCK_VIEW', '')
    if not path:
        return

    if not '.' in path:
        return

    module_path, view_name = path.rsplit('.', 1)
    try:
        module = import_module(module_path)
    except ImportError:
        return

    view = getattr(module, view_name, None)
    setattr(block, '_BLOCK_VIEW', staticmethod(view))
    return view
