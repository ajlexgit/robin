from django.db import models
from django.template import Library
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ..models import AttachableBlock, AttachableReference
from ..register import get_block_subclass
from ..utils import get_block_view

register = Library()


@register.simple_tag(takes_context=True)
def render_attached_blocks(context, entity, set_name=None):
    request = context.get('request')
    if not request:
        return ''

    ct = ContentType.objects.get_for_model(entity)
    query = models.Q(block__visible=True, content_type=ct, object_id=entity.pk)
    if set_name:
        query &= models.Q(set_name=set_name)
    block_refs = AttachableReference.objects.filter(query)

    output = []
    for block_ref in block_refs:
        try:
            real_block = get_block_subclass(block_ref.block)
        except ObjectDoesNotExist:
            continue

        block_view = get_block_view(real_block)
        if not block_view:
            continue

        output.append(
            block_view(request, real_block)
        )

    return ''.join(output)


@register.simple_tag(takes_context=True)
def render_attachable_block(context, block, **kwargs):
    request = context.get('request')
    if not request:
        return ''

    if not isinstance(block, AttachableBlock):
        return ''

    if not block.visible:
        return ''

    block_view = get_block_view(block)
    if not block_view:
        return ''

    return block_view(request, block, **kwargs)