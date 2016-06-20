from django.apps import apps
from django.template import Library
from ..utils import get_block, get_block_view, get_visible_references

register = Library()


def block_output(request, block, ajax=False, **kwargs):
    block_view = get_block_view(block)
    if not block_view:
        return ''

    if ajax:
        # Блок, загружаемый через AJAX
        block_html = '<div class="async-block" data-id="%s"></div>' % block.id
    else:
        block_html = block_view(request, block, **kwargs)

    return block_html


@register.simple_tag(takes_context=True)
def render_attached_blocks(context, entity, set_name='default'):
    request = context.get('request')
    if not request:
        return ''

    output = []
    for blockref in get_visible_references(entity, set_name=set_name).only('block_ct', 'block_id', 'ajax'):
        block = get_block(blockref.block_id, ct=blockref.block_ct)
        if not block:
            continue

        block_html = block_output(request, block, blockref.ajax)
        if block_html:
            output.append(block_html)

    return ''.join(output)


@register.simple_tag(takes_context=True)
def render_attachable_block(context, block, ajax=False, **kwargs):
    request = context.get('request')
    if not request:
        return ''

    if not block:
        return ''

    real_block = get_block(block.id)
    if not real_block or not real_block.visible:
        return ''

    return block_output(request, real_block, ajax, **kwargs)


@register.simple_tag(takes_context=True)
def render_first_attachable_block(context, model, ajax=False, **kwargs):
    if not '.' in model:
        return ''

    app, modelname = model.rsplit('.', 1)
    try:
        model = apps.get_model(app, modelname)
    except LookupError:
        return ''

    block = model.objects.first()
    if not block:
        return ''

    return render_attachable_block(context, block, ajax)
