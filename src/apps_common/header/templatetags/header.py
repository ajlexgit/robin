from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def header(context, template='header/header.html'):
    """ Шапка """
    return loader.render_to_string(template, {
        
    }, request=context.get('request'))
