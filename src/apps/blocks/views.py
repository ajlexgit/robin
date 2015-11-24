def render_first_block(request, block):
    return '<div class="block-1">%s</div>' % block.label


def render_second_block(request, block):
    return '<div class="block-2">%s</div>' % block.label
