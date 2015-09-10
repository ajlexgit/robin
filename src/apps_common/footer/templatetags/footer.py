from django.template import Library, loader, RequestContext

register = Library()


@register.simple_tag(takes_context=True)
def footer(context, template='footer/footer.html'):
    """ Футер """
    request = context.get('request')
    if not request:
        return ''

    return loader.render_to_string(template, {
    
    }, context_instance=RequestContext(request))
