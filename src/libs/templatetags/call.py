from django.template import Library, Node, TemplateSyntaxError
from django.template.base import token_kwargs

register = Library()

"""
    Шаблонный тэг call, позволяющий получить результат вызова метода в переменную.
    Первый аргумент должен быть методом объекта, содержащим точку.
    Предпоследний аргумент должен быть ключевым словом 'as'.
    Последний аргумент - имя переменной, в которую будет сохранен результат.

    Полный формат тэга:
        {% call <instancee_method> <arg1> .. <argN> <kwarg1> .. <kwargN> as <variable> %}

    Пример:
        {% call comment.can_edit request.user as can_edit_comment %}
"""


class CallNode(Node):
    def __init__(self, instance, method_name, args, kwargs, target_var):
        self.instance = instance
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        self.target_var = target_var

    def render(self, context):
        instance = self.instance.resolve(context)
        method = getattr(instance, self.method_name)

        resolved_args = [var.resolve(context) for var in self.args]
        resolved_kwargs = dict((k, v.resolve(context)) for k, v in self.kwargs.items())

        context[self.target_var] = method(*resolved_args, **resolved_kwargs)
        return ''


@register.tag
def call(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) < 3 or bits[-2] != 'as':
        raise TemplateSyntaxError(
            "'call' tag takes at least 3 arguments and the "
            "second last argument must be 'as'")

    method = bits[0].rsplit('.', 1)
    if len(method) < 2:
        raise TemplateSyntaxError(
            "first argument of 'call' tag should contain '.'")

    target_var = bits[-1]
    bits = bits[1:-2]

    instance, method_name = method
    instance = parser.compile_filter(instance)

    # args and kwargs
    args = []
    kwargs = {}
    for bit in bits:
        kwarg = token_kwargs([bit], parser)
        if kwarg:
            param, value = list(kwarg.items())[0]
            kwargs[str(param)] = value
        else:
            args.append(parser.compile_filter(bit))

    return CallNode(instance, method_name, args, kwargs, target_var)
