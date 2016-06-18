from django.core.cache import caches
from datetime import datetime, timedelta
from django.core.cache.utils import make_template_fragment_key
from django.template import Library, Node, TemplateSyntaxError, VariableDoesNotExist
from .. import conf

register = Library()
cache = caches[conf.AJAXCACHE_BACKEND]


class CacheNode(Node):
    def __init__(self, nodelist, expire_time_var, fragment_name, vary_on):
        self.nodelist = nodelist
        self.expire_time_var = expire_time_var
        self.fragment_name = fragment_name
        self.vary_on = vary_on

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"ajaxcache" tag got an unknown variable: %r' % self.expire_time_var.var)
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"ajaxcache" tag got a non-integer timeout value: %r' % expire_time)

        if expire_time < 120:
            raise TemplateSyntaxError('"ajaxcache" tag got a timeout less than 120: %r' % expire_time)

        vary_on = [var.resolve(context) for var in self.vary_on]
        cache_key = make_template_fragment_key(self.fragment_name, vary_on)
        value = cache.get(cache_key)

        expiration_key = 'expire.%s' % cache_key
        expiration_date = cache.get(expiration_key)

        if value is None or expiration_date is None or expiration_date <= datetime.now():
            value = self.nodelist.render(context)
            expiration_date = datetime.now() + timedelta(seconds=expire_time - conf.AJAXCACHE_GAP)

            cache.set('time.%s' % cache_key, expire_time, expire_time)
            cache.set(expiration_key, expiration_date, expire_time)
            cache.set(cache_key, value, expire_time)
        return '<div class="%s" data-key="%s"></div>' % (conf.AJAXCACHE_CSS_CLASS, cache_key)


@register.tag('ajaxcache')
def do_cache(parser, token):
    nodelist = parser.parse(('endajaxcache',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError("'%r' tag requires at least 2 arguments." % tokens[0])
    return CacheNode(nodelist,
        parser.compile_filter(tokens[1]),
        tokens[2],  # fragment_name can't be a variable.
        [parser.compile_filter(t) for t in tokens[3:]],
    )
