import re
from hashlib import md5
from datetime import datetime, timedelta
from django.core.cache import caches
from django.template import Library, Node, TemplateSyntaxError, VariableDoesNotExist
from .. import conf

register = Library()

TOKEN_NAME = 'cacheblock'
cache = caches[conf.CACHEBLOCK_BACKEND]
re_ajax = re.compile('ajax=(.+)', re.IGNORECASE)


class CacheNode(Node):
    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on, is_ajax=None):
        self.nodelist = nodelist
        self.expire_time_var = expire_time_var
        self.fragment_name = fragment_name
        self.vary_on = vary_on
        self.is_ajax = is_ajax

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"%s" tag got an unknown variable: %r' % (TOKEN_NAME, self.expire_time_var.var))
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"%s" tag got a non-integer timeout value: %r' % (TOKEN_NAME, expire_time))

        if expire_time < 120:
            raise TemplateSyntaxError('"%s" tag got a timeout less than 120: %r' % (TOKEN_NAME, expire_time))

        vary_on = [var.resolve(context) for var in self.vary_on]

        vary_key = md5(':'.join(str(var) for var in vary_on).encode()).hexdigest()
        cache_key = '%s.%s' % (self.fragment_name, vary_key)
        value = cache.get(cache_key)

        expiration_key = 'expire.%s' % cache_key
        expiration_date = cache.get(expiration_key)

        if not conf.CACHEBLOCK_ENABLED or value is None or expiration_date is None or expiration_date <= datetime.now():
            value = self.nodelist.render(context)
            expiration_date = datetime.now() + timedelta(seconds=expire_time - conf.CACHEBLOCK_GAP)

            cache.set('time.%s' % cache_key, expire_time, expire_time)
            cache.set(expiration_key, expiration_date, expire_time)
            cache.set(cache_key, value, expire_time)

        is_ajax = self.is_ajax and self.is_ajax.resolve(context)
        if is_ajax:
            return '<div class="%s" data-key="%s"></div>' % (conf.CACHEBLOCK_CSS_CLASS, cache_key)
        else:
            return value


@register.tag(TOKEN_NAME)
def do_cache(parser, token):
    nodelist = parser.parse(('end' + TOKEN_NAME,))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError('"%s" tag requires at least 2 arguments.' % TOKEN_NAME)

    params = []
    is_ajax = None
    for param in tokens[3:]:
        match = re_ajax.match(param)
        if match:
            is_ajax = parser.compile_filter(match.group(1))
        else:
            params.append(parser.compile_filter(param))

    return CacheNode(nodelist,
        parser.compile_filter(tokens[1]),
        tokens[2],  # fragment_name can't be a variable.
        params,
        is_ajax,
    )
