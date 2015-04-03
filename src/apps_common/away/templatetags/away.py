from django import template
from ..away import away_links

register = template.Library()


@register.simple_tag(takes_context=True)
def away(context, html):
    return away_links(context['request'], html)
