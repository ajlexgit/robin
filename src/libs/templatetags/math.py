from operator import truediv
from django.template import Library

register = Library()


@register.filter
def mul(value, arg):
    return value * arg


@register.filter
def tuplediv(value):
    return truediv(*value)
