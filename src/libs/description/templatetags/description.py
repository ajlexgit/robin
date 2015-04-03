from django.template import Library
from ..description import *

register = Library()


@register.filter(name="description")
def description_filter(value, args):
    """
    Собираем параграфы до достижения заданной длины.
    Если недобрали - добираем предложениями из следующего параграфа.

    Принимает текст, разделенный на параграфы символом перевода строки.

    Пример:
        {{ text|description:"100, 150" }}
    """
    args = args.split(',')
    if len(args) == 1:
        args = [0, args[0]]
    args = [int(arg.strip()) for arg in args]
    return description(value, *args)


@register.filter(name="strip_tags_except")
def strip_tags_except_filter(value, args):
    """
    Удаление HTML-тэгов, кроме перечисленных в valid_tags.

    Пример:
        {{ text|strip_tags_except:"a, p" }}
    """
    return strip_tags_except(value, [item.strip() for item in args.split(',')])
