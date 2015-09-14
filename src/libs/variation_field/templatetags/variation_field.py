from django.template import Library

register = Library()


@register.filter
def get_variation(value, arg):
    """
        Получение вариации по имени.
        Если не найдена - возвращается оригинал.
        Пример:
            {% with variation_field=image|get_variation:'normal' %}
                {{ variation_field.url }}
            {% endwith %}
    """
    return getattr(value, arg, value) if arg else value
