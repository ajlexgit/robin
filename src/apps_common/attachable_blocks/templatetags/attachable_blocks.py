from django.template import Library
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ..models import AttachableBlockRef
from ..register import get_block_subclass, get_block_renderer

register = Library()


@register.simple_tag(takes_context=True)
def render_attached_blocks(context, entity):
    request = context.get('request')
    if not request:
        return ''

    ct = ContentType.objects.get_for_model(entity)
    block_refs = AttachableBlockRef.objects.filter(
        block__visible=True,
        content_type=ct,
        object_id=entity.pk,
    )

    output = []
    for block_ref in block_refs:
        try:
            real_block = get_block_subclass(block_ref.block)
        except ObjectDoesNotExist:
            continue

        render_func = get_block_renderer(block_ref.block)
        if not render_func:
            continue

        output.append(
            render_func(request, real_block)
        )

    return ''.join(output)