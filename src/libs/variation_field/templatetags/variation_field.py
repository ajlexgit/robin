from django.template import Library

register = Library()


@register.filter
def variation_field(value, arg):
    """
    Получение вариации по имени.
    Если не найдена - возвращается оригинал.
    Пример:
        {% with variation_field=image|variation_field:'normal' %}
            {{ variation_field.url }}
        {% endwith %}
    """
    return getattr(value, arg, value) if arg else value