from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def footer(context, template='footer/footer.html'):
    """ Футер """
    return loader.render_to_string(template, {
        
    }, request=context.get('request'))
