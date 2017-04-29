from django.apps import apps
from django.template import Library
from ..models import AttachableBlock, AttachableReference
from ..utils import get_model_by_ct, get_block_view

register = Library()


def block_output(context, block, ajax=False, **kwargs):
    """
        Возвращает отрендеренный HTML блока или заглушку для AJAX-запроса
    """
    block_view = get_block_view(block)
    if not block_view:
        return ''

    if ajax:
        # Блок, загружаемый через AJAX
        block_html = '<div class="async-block" data-id="%s"></div>' % block.id
    else:
        block_html = block_view(context, block, **kwargs)

    return block_html


@register.simple_tag(takes_context=True)
def render_attached_blocks(context, entity, set_name='default', **kwargs):
    output = []
    kwargs.setdefault('instance', entity)

    references = AttachableReference.get_for(entity, set_name=set_name)
    for reference in references.only('block_ct', 'block_id', 'ajax'):
        block_model = get_model_by_ct(reference.block_ct_id)
        block = block_model.objects.get(pk=reference.block_id)

        block_html = block_output(context, block, ajax=reference.ajax, **kwargs)
        if block_html:
            output.append(block_html)

    return ''.join(output)


@register.simple_tag(takes_context=True)
def render_attachable_block(context, block, ajax=False, **kwargs):
    if block is None:
        return ''

    if block._meta.concrete_model is AttachableBlock:
        block_model = get_model_by_ct(block.block_content_type_id)
        block = block_model.objects.get(pk=block.pk)

    if block.visible:
        return block_output(context, block, ajax=ajax, **kwargs)
    else:
        return ''


@register.simple_tag(takes_context=True)
def render_first_attachable_block(context, model_path, ajax=False, **kwargs):
    if '.' not in model_path:
        return ''

    app, modelname = model_path.rsplit('.', 1)
    try:
        model = apps.get_model(app, modelname)
    except LookupError:
        return ''

    block = model.objects.first()
    if not block:
        return ''

    return render_attachable_block(context, block, ajax=ajax, **kwargs)
