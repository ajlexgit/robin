from .utils import get_model, get_block_type

_BLOCK_NAMES = {}
_BLOCK_RENDERERS = {}


def register_block(name=None):
    """ Регистрация модели нового блока """
    def decorator(block_cls):
        block_id = get_block_type(block_cls)
        block_name = name or block_cls._meta.verbose_name_plural
        _BLOCK_NAMES[block_id] = block_name
        return block_cls
    return decorator


def register_block_renderer(block_cls):
    """ Задает блоку функцию рендеринга """
    block_id = get_block_type(block_cls)
    def decorator(func):
        _BLOCK_RENDERERS[block_id] = func
        return func
    return decorator


def get_block_choices():
    """ Получение вариантов типа блока для селектов """
    for key, value in sorted(_BLOCK_NAMES.items(), key=lambda x: x[1]):
        yield (key, value)


def get_block_subclass(block):
    """ Получение конкретного блока по экземпляру базового класса блока """
    BlockModel = get_model(block.block_type)
    return BlockModel.objects.get(pk=block.block.pk)


def get_block_renderer(block):
    """ Получение функции рендеринга конкретного блока по экземпляру базового класса блока """
    return _BLOCK_RENDERERS.get(block.block_type)