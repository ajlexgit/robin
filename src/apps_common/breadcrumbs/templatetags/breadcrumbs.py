from django.template import Library
from ..views import render_breadcrumbs

register = Library()


@register.simple_tag(takes_context=True)
def breadcrumbs(context, template=None):
    request = context['request']
    return render_breadcrumbs(request.breadcrumbs, template)