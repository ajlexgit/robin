from importlib import import_module


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


def get_block(block_id):
    """
        Получение блока реального типа по его ID
    """
    from .models import AttachableBlock
    return AttachableBlock.objects.filter(pk=block_id).select_subclasses().first()
