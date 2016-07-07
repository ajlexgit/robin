from django.template import Library

register = Library()


@register.simple_tag
def href(paginator, number):
    """ Генерация ссылки на страницу навигации """
    if number == 1:
        link = '?'
    else:
        link = '?%s=%s' % (paginator.parameter_name, number)

    if paginator.anchor:
        link += '#' + paginator.anchor

    return link
