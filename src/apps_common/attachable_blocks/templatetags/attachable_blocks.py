from django.db import models
from django.template import Library
from django.contrib.contenttypes.models import ContentType
from ..models import AttachableReference
from ..utils import get_block, get_block_view

register = Library()


@register.simple_tag(takes_context=True)
def render_attached_blocks(context, entity, set_name=None):
    request = context.get('request')
    if not request:
        return ''

    ct = ContentType.objects.get_for_model(entity)
    query = models.Q(
        content_type=ct,
        object_id=entity.pk,
        block__visible=True
    )
    if set_name:
        query &= models.Q(set_name=set_name)
    block_ids = AttachableReference.objects.filter(query).values_list('block_id', flat=True)

    output = []
    for block_id in block_ids:
        block = get_block(block_id)
        if not block:
            continue

        block_view = get_block_view(block)
        if not block_view:
            continue

        output.append(
            block_view(request, block)
        )

    return ''.join(output)


@register.simple_tag(takes_context=True)
def render_attachable_block(context, block):
    request = context.get('request')
    if not request:
        return ''

    real_block = get_block(block.id)
    if not real_block or not real_block.visible:
        return ''

    block_view = get_block_view(real_block)
    if not block_view:
        return ''

    return block_view(request, real_block)