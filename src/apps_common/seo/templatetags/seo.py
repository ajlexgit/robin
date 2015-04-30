from django.template import loader, Library

register = Library()


@register.simple_tag(takes_context=True)
def seo_block(context, template='seo/block.html'):
    request = context['request']
    if not request.seo or not request.seo.instance:
        return ''

    return loader.render_to_string(template, {
        'instance': request.seo.instance,
    })