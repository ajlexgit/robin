import re
from html import unescape
from bs4 import BeautifulSoup as Soup
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

re_pred = re.compile('\\b([\'\"\w]{1,3})\s+')


def typograf_text(text):
    return re_pred.sub('\\1&nbsp;', text)

@register.filter
def typograf(html):
    soup = Soup(html)

    for tag in soup.findAll(text=True):
        new_tag = soup.new_string(unescape(re_pred.sub('\\1&nbsp;', tag)))
        tag.replace_with(new_tag)

    body = soup.body.contents if soup.body else soup
    text = ''.join(str(tag) for tag in body)
    text = text.replace('\u200b', '').strip()
    return mark_safe(text)