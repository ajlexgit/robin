import re
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

re_spaces = re.compile('\n([ \r\t\xa0]*\n)+')

@register.filter
def paragraphs(text):
    text = re_spaces.sub('\n', text.strip())
    paragraphs = '<p>' + '</p><p>'.join(text.split('\n')) + '</p>'
    return mark_safe(paragraphs)