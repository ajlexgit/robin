from django.template import loader, RequestContext


def my_block_render(request, block):
    context = RequestContext(request, {
        'block': block,
    })
    return loader.render_to_string('blocks/block.html', context_instance=context)

