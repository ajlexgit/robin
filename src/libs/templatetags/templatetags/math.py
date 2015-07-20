from operator import truediv
from django.template import Library

register = Library()


@register.filter(is_safe=True)
def mul(value, arg):
    return value * arg


@register.filter(is_safe=True)
def tuplediv(value):
    return truediv(*value)
