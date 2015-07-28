from django.template import loader, Library
from libs.description import description
from ..models import Counter

register = Library()


@register.simple_tag(takes_context=True)
def seo_block(context, template='seo/block.html'):
    request = context.get('request')
    if not request:
        return ''

    if not request.seo or not request.seo.instance:
        return ''

    seo_instance = request.seo.instance
    full = seo_instance.text.strip()
    if not full:
        return ''

    short = description(seo_instance.text, 500, 800)

    return loader.render_to_string(template, {
        'instance': seo_instance,
        'full_text': full,
        'short_text': short,
        'animated': len(full) > len(short),
    })


@register.simple_tag
def seo_counters(position):
    counters = Counter.objects.filter(position=position)
    if not counters:
        return ''

    content = '\n'.join(c.content for c in counters)
    return content
