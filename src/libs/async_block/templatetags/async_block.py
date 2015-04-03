from importlib import import_module
from urllib.parse import urlencode
from django.template import Library, loader
from django.core.urlresolvers import resolve, reverse

register = Library()


def _get_view_by_url(url):
    """ Получение объекта View по имени урла """
    resolver_match = resolve(url)

    view_module = import_module(resolver_match.func.__module__)
    view_name = resolver_match.func.__name__

    view_class = getattr(view_module, view_name)
    return view_class()


@register.simple_tag
def async_block(url_name, **kwargs):
    """
    Асинхронный блок.
    Все параметры, кроме имеющих значение None, передаются через GET.

    Пример:
        {% async_block 'news:block' id=new.id count=5 %}
    """
    params = filter(lambda x: x[1] is not None, kwargs.items())
    return loader.render_to_string('async_block.html', {
        'id': url_name.replace(':', '-'),
        'url': reverse(url_name) + '?' + urlencode(tuple(params)),
    })


@register.simple_tag(takes_context=True)
def sync_block(context, url_name, **kwargs):
    """
    Синхронный блок.
    Используется для организации вывода блока синхронно.
    Все параметры, кроме имеющих значение None, передаются через kwargs.

    Пример:
        {% if request.is_ajax %}
            {% sync_block 'news:block' id=new.id count=5 %}
        {% else %}
            {% async_block 'news:block' id=new.id count=5 %}
        {% endif %}
    """
    params = filter(lambda x: x[1] is not None, kwargs.items())
    view = _get_view_by_url(reverse(url_name))
    return view.sync_render(context['request'], **dict(params))
