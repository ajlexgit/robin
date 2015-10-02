from collections import OrderedDict
from inspect import isclass
from .utils import get_model, get_block_type

_BLOCK_NAMES = OrderedDict()


def register_block(name=None):
    """ Регистрация модели нового блока """
    def decorator(block_cls):
        block_id = get_block_type(block_cls)
        block_name = name or block_cls._meta.verbose_name_plural
        _BLOCK_NAMES[block_id] = block_name
        return block_cls

    if isclass(name):
        cls = name
        name = None
        return decorator(cls)

    return decorator


def get_block_choices():
    """ Получение вариантов типа блока для селектов """
    for key, value in sorted(_BLOCK_NAMES.items(), key=lambda x: x[1]):
        yield (key, value)


def get_block_subclass(block):
    """ Получение конкретного блока по экземпляру базового класса блока """
    BlockModel = get_model(block.block_type)
    return BlockModel.objects.get(pk=block.pk)
