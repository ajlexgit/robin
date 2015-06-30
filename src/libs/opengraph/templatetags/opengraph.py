from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def opengraph(context):
    request = context.get('request')
    if not request:
        return ''

    return request.opengraph.render()
