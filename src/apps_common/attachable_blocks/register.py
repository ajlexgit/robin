from.utils import get_model

_BLOCK_NAMES = {}
_BLOCK_RENDERERS = {}


def register_block(name=None):
    """ Регистрация модели нового блока """
    def decorator(cls):
        block_id = '%s.%s' % (cls.__module__, cls.__qualname__)
        block_name = name or cls._meta.verbose_name_plural
        _BLOCK_NAMES[block_id] = block_name
        return cls
    return decorator


def register_block_renderer(cls):
    """ Задает блоку функцию рендеринга """
    block_id = '%s.%s' % (cls.__module__, cls.__qualname__)
    def decorator(func):
        _BLOCK_RENDERERS[block_id] = func
        return func
    return decorator


def get_block_choices():
    """ Получение вариантов типа блока для селектов """
    for key, value in _BLOCK_NAMES.items():
        yield (key, value)


def get_block_subclass(block):
    """ Получение конкретного блока по экземпляру базового класса блока """
    BlockModel = get_model(block.block_model)
    return BlockModel.objects.get(pk=block.block.pk)


def get_block_renderer(block):
    """ Получение функции рендеринга конкретного блока по экземпляру базового класса блока """
    return _BLOCK_RENDERERS.get(block.block_model)