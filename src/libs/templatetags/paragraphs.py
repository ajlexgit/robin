import re
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

re_newlines = re.compile('[ \r\t\xa0]*\n')
re_many_newlines = re.compile('\n{2,}')


@register.filter
def paragraphs(text):
    text = re_newlines.sub('\n', text)
    text = re_many_newlines.sub('\n', text)
    result = '<p>' + '</p><p>'.join(text.strip().split('\n')) + '</p>'
    return mark_safe(result)