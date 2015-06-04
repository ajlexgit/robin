import re
from html import unescape
from bs4 import BeautifulSoup as Soup, NavigableString
from django.template import Library, defaultfilters
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = Library()

re_nbsp = re.compile('\\b([\'\"\w]{1,3})\s+')
re_clean_newlines = re.compile('[ \r\t\xa0]*\n')
re_many_newlines = re.compile('\n{2,}')



@register.filter(name="striptags_except")
def strip_tags_except_filter(value, args):
    """
        Удаление HTML-тэгов, кроме перечисленных в valid_tags.

        Пример:
            {{ text|striptags_except:"a, p" }}
    """
    valid_tags = [item.strip() for item in args.split(',')]

    def process_tag(tag):
        if isinstance(tag, NavigableString):
            return tag

        if tag.name in valid_tags:
            for subtag in tag.contents:
                subtag.replaceWith(process_tag(subtag))
            return tag
        else:
            result = ""
            for subtag in tag.contents:
                result += str(process_tag(subtag))
            return result

    soup = Soup(value, 'html5lib')
    body = soup.body.contents if soup.body else soup

    for tag in body:
        tag.replaceWith(process_tag(tag))

    body = soup.body.contents if soup.body else soup
    text = '\n'.join(str(tag) for tag in body)
    return re_clean_newlines.sub('\n', text.strip())


@register.filter(is_safe=True)
def typograf(html):
    """
        Удаление висячих предлогов
    """
    soup = Soup(html, 'html5lib')

    for tag in soup.findAll(text=True):
        new_tag = soup.new_string(unescape(re_nbsp.sub('\\1&nbsp;', tag)))
        tag.replace_with(new_tag)

    body = soup.body.contents if soup.body else soup
    text = ''.join(str(tag) for tag in body)
    return text.strip()


@register.filter
def paragraphs(text):
    """
        Разбивка текста на параграфы в местах переносов строк
    """
    text = re_clean_newlines.sub('\n', text)
    text = re_many_newlines.sub('\n', text)
    result = '<p>' + '</p><p>'.join(text.strip().split('\n')) + '</p>'
    return result


@register.filter
def clean(html):
    """
        Алиас для трех фильтров: VLAUE|striptags|linebreaksbr|typograf|safe
    """
    text = strip_tags(html)
    text = defaultfilters.linebreaksbr(text)
    text = typograf(text)
    return mark_safe(text)