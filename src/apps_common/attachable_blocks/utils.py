from importlib import import_module
from django.db import models
from django.apps import apps
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType


def get_block_types():
    """
        Возвращает список content_type_id всех блоков из кэша
    """
    from .models import AttachableBlock

    if 'attachable_block_types' not in cache:
        blocks = []
        for model in apps.get_models():
            if issubclass(model, AttachableBlock) and model != AttachableBlock:
                ct = ContentType.objects.get_for_model(model)
                blocks.append((ct.pk, str(model._meta.verbose_name)))

        blocks = tuple(sorted(blocks, key=lambda x: x[1]))
        cache.set('attachable_block_types', blocks, timeout=10 * 60)

    return cache.get('attachable_block_types')


def get_visible_references(instance, set_name=None):
    """
        Получение связей на видимые блоки для сущности
    """
    from .models import AttachableReference

    ct = ContentType.objects.get_for_model(instance)
    query = models.Q(
        content_type=ct,
        object_id=instance.pk,
        block__visible=True,
    )

    if set_name is not None:
        query &= models.Q(set_name=set_name)

    return AttachableReference.objects.filter(query)


def get_last_updated(instance):
    """
        Получение даты последнего изменения подключаемого блока,
        привязанного к сущности
    """
    from .models import AttachableBlock
    attached_blocks = get_visible_references(instance).values_list('block', flat=True)
    result = AttachableBlock.objects.filter(pk__in=attached_blocks).aggregate(models.Max('updated'))
    return result['updated__max']


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


def get_block(block_id, ct=None):
    """
        Получение блока реального типа по его ID
    """
    from .models import AttachableBlock
    if ct is None:
        # Fallback
        return AttachableBlock.objects.filter(pk=block_id).select_subclasses().first()
    else:
        # Ускоренная выборка
        return ct.get_object_for_this_type(pk=block_id)
