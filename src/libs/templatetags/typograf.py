import re
from django.template import Library, defaultfilters
from django.utils.safestring import mark_safe

register = Library()

re_pred = re.compile('\\b([\'\"\w]{1,3})\s+')


@register.filter
def typograf(value):
    text = defaultfilters.striptags(value)
    text = re_pred.sub('\\1&nbsp;', text)
    text = defaultfilters.linebreaksbr(text)

    return mark_safe(text)