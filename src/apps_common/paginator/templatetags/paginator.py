from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def paginator(context, obj):
    request = context.get('request')

    if not obj.current_page.has_other_pages():
        return ''

    return loader.render_to_string(obj.template, {
        'paginator': obj,
        'page': obj.current_page,
    }, request=request)


@register.simple_tag(takes_context=True)
def href(context, paginator, number):
    """ Генерация ссылки на страницу навигации """
    if number == 1:
        request = context.get('request')
        if request:
            link = request.path_info
        else:
            link = '?'
    else:
        link = '?%s=%s' % (paginator.parameter_name, number)

    if paginator.anchor:
        link += '#' + paginator.anchor

    return link
