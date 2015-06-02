import re
from html import unescape
from bs4 import BeautifulSoup as Soup
from django.template import Library, defaultfilters
from django.utils.html import strip_tags

register = Library()

re_pred = re.compile('\\b([\'\"\w]{1,3})\s+')
re_newlines = re.compile('[ \r\t\xa0]*\n')
re_many_newlines = re.compile('\n{2,}')


@register.filter(is_safe=True)
def clear_text(html):
    text = strip_tags(html)
    return defaultfilters.linebreaksbr(text)


@register.filter(is_safe=True)
def typograf(html):
    soup = Soup(html)

    for tag in soup.findAll(text=True):
        new_tag = soup.new_string(unescape(re_pred.sub('\\1&nbsp;', tag)))
        tag.replace_with(new_tag)

    body = soup.body.contents if soup.body else soup
    text = ''.join(str(tag) for tag in body)
    return text.strip()


@register.filter(is_safe=True)
def paragraphs(text):
    text = re_newlines.sub('\n', text)
    text = re_many_newlines.sub('\n', text)
    result = '<p>' + '</p><p>'.join(text.strip().split('\n')) + '</p>'
    return result