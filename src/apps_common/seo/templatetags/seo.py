from django.template import loader, Library
from ..models import Counter
from ..seo import Seo

register = Library()


@register.simple_tag(takes_context=True)
def seo_block(context, entity=None, template='seo/block.html'):
    request = context.get('request')
    if not request or not request.seo:
        return ''

    if entity:
        seodata = Seo.get_for(entity)
    else:
        seodata = getattr(request, 'seodata', None)

    if not seodata or not seodata.text:
        return ''

    return loader.render_to_string(template, {
        'data': seodata,
    })


@register.simple_tag
def seo_counters(position):
    counters = Counter.objects.filter(position=position)
    if not counters:
        return ''

    content = '\n'.join(c.content for c in counters)
    return content
