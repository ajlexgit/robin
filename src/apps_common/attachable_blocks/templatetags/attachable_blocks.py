from django.core.exceptions import ObjectDoesNotExist
from django.template import Library
from ..register import get_block_subclass, get_block_renderer

register = Library()


@register.simple_tag(takes_context=True)
def render_blocks(context, entity):
    request = context.get('request')
    if not request:
        return ''

    if not hasattr(entity, 'blocks'):
        return ''

    block_refs = entity.blocks.through.objects.filter(block__visible=True)

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