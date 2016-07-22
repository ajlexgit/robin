from django.template import loader, Library
from ..models import Service

register = Library()


@register.simple_tag(takes_context=True)
def services_block(context):
    context.update({
        'services': Service.objects.all(),
    })
    return loader.render_to_string('services/block.html', context)
