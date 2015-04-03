from django.template import add_to_builtins

# Подгружаем фильтры во все шаблоны
add_to_builtins('%s.%s' % (__name__, 'call'))
add_to_builtins('%s.%s' % (__name__, 'math'))
add_to_builtins('%s.%s' % (__name__, 'json'))
add_to_builtins('%s.%s' % (__name__, 'dates'))