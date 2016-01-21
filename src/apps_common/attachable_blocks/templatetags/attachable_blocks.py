from django.apps import apps
from django.db import models
from django.template import Library
from django.contrib.contenttypes.models import ContentType
from ..models import AttachableReference
from ..utils import get_block, get_block_view

register = Library()


def block_output(request, block, noindex=False, ajax=False):
    block_view = get_block_view(block)
    if not block_view:
        return ''

    if ajax:
        # Блок, загружаемый через AJAX
        block_html = '<div class="async-block" data-id="%s"></div>' % block.id
    else:
        block_html = block_view(request, block)

    if noindex:
        return ''.join(('<!--noindex-->', block_html, '<!--/noindex-->',))
    else:
        return block_html


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

    output = []
    for blockref in AttachableReference.objects.filter(query):
        block = get_block(blockref.block_id)
        if not block:
            continue

        block_html = block_output(request, block, blockref.noindex, blockref.ajax)
        if block_html:
            output.append(block_html)

    return ''.join(output)


@register.simple_tag(takes_context=True)
def render_attachable_block(context, block, noindex=False, ajax=False):
    request = context.get('request')
    if not request:
        return ''

    real_block = get_block(block.id)
    if not real_block or not real_block.visible:
        return ''

    return block_output(request, real_block, noindex, ajax)


@register.simple_tag(takes_context=True)
def render_first_attachable_block(context, model, noindex=False, ajax=False):
    if not '.' in model:
        return ''

    app, modelname = model.rsplit('.', 1)
    try:
        model = apps.get_model(app, modelname)
    except LookupError:
        return ''

    return render_attachable_block(context, model.objects.first(), noindex, ajax)
