from django.template import loader, RequestContext


def sample_block_render(request, block):
    context = RequestContext(request, {
        'block': block,
    })
    return loader.render_to_string('blocks/sample_block.html', context_instance=context)
