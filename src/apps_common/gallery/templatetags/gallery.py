from django.template import loader, Library

register = Library()
    

@register.simple_tag
def gallery(gallery_instance, template='gallery/gallery.html'):
    return loader.render_to_string(template, {
        'gallery': gallery_instance,
    })