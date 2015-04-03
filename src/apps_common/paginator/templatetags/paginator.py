from django.template import Library

register = Library()


@register.simple_tag
def href(paginator, number):
    """ Генерация ссылки на страницу навигации """
    number = paginator.real_page_number(number)
    return paginator.href(number)
