from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def opengraph(context):
    request = context.get('request')
    if not request:
        return ''

    output = []
    og = getattr(request, 'opengraph', None)
    if og is not None:
        output.append(og.render())

    tw = getattr(request, 'twitter_card', None)
    if tw is not None:
        output.append(tw.render())

    return ''.join(output)
