from urllib import parse as urlparse
from django.template import loader, Library
from ..services import SERVICES

register = Library()

@register.simple_tag(takes_context=True)
def social_share(context, service_name, **kwargs):
    request = context.get('request')
    if not request:
        return ''

    service = SERVICES.get(service_name)
    if not service:
        return ''

    # Собираем данные из Opengraph и аргументов
    params_in = {
        'url': request.build_absolute_uri(request.path),
    }
    if hasattr(request, 'opengraph'):
        params_in.update(request.opengraph)
    params_in.update(kwargs)

    # Абсолютный адрес для картинки
    if 'image' in params_in:
        params_in['image'] = request.build_absolute_uri(params_in['image'])

    params_out = {}
    for name, param_name in service['allowed_params'].items():
        if name in params_in and params_in[name]:
            value = params_in[name]
            if 'modifiers' in service and name in service['modifiers']:
                params_out[param_name] = service['modifiers'][name](**params_in)
            else:
                params_out[param_name] = value

    # Формируем URL
    params = urlparse.urlencode(params_out)
    url_parts = list(urlparse.urlparse(service['endpoint']))
    url_parts[4] += '&' + params if url_parts[4] else params
    final_url = urlparse.urlunparse(url_parts)

    return loader.render_to_string('social_buttons/button.html', {
        'service': service,
        'url': final_url,
    })
