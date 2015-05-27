from django.template import loader, Library
from django.utils.safestring import mark_safe
from ..models import Counter

register = Library()


@register.simple_tag(takes_context=True)
def seo_block(context, template='seo/block.html'):
    request = context.get('request')
    if not request:
        return ''

    if not request.seo or not request.seo.instance:
        return ''

    return loader.render_to_string(template, {
        'instance': request.seo.instance,
    })


@register.simple_tag
def seo_counters(position):
    counters = Counter.objects.filter(position=position)
    if not counters:
        return ''

    content = '\n'.join(c.content for c in counters)
    return mark_safe(content)