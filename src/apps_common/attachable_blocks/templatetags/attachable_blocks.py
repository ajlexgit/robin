from django.template import Library
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ..models import AttachableBlockRef
from ..register import get_block_subclass
from ..utils import get_block_view

register = Library()


@register.simple_tag(takes_context=True)
def render_attached_blocks(context, entity, frame=0):
    request = context.get('request')
    if not request:
        return ''

    ct = ContentType.objects.get_for_model(entity)
    block_refs = AttachableBlockRef.objects.filter(
        block__visible=True,
        content_type=ct,
        object_id=entity.pk,
        frame=frame
    )

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
