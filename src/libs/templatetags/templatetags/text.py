import re
from html import unescape
from bs4 import BeautifulSoup as Soup, NavigableString
from softhyphen.html import get_hyphenator_for_language, SOFT_HYPHEN
from django.conf import settings
from django.core.cache import caches
from django.utils.html import strip_tags, escape
from django.utils.safestring import mark_safe
from django.template import Library, defaultfilters

register = Library()

re_nbsp = re.compile('\\b(\w{1,3})\s+')
re_clean_newlines = re.compile('[ \r\t\xa0]*\n')
re_many_newlines = re.compile('\n{2,}')

hybernator = get_hyphenator_for_language(settings.LANGUAGE_CODE)
hybernator.left = 4
hybernator.right = 3


def hybernate_string(string):
    result = (
        hybernator.inserted(word, SOFT_HYPHEN)
        for word in string.split()
    )
    return ' '.join(result)


def process_tag(tag, valid_tags=()):
    if isinstance(tag, NavigableString):
        return tag

    if tag.name in valid_tags:
        for subtag in tag.contents:
            subtag.replaceWith(process_tag(subtag, valid_tags))
        return tag
    else:
        result = ""
        for subtag in tag.contents:
            result += str(process_tag(subtag, valid_tags))
        return result


@register.filter(is_safe=True, name="striptags_except")
def strip_tags_except_filter(html, args):
    """
        Удаление HTML-тэгов, кроме перечисленных в аргументе.

        Пример:
            {{ text|striptags_except:"a, p" }}
    """
    valid_tags = [item.strip() for item in args.split(',')]

    soup = Soup(html, 'html5lib')

    for tag in soup.body:
        tag.replaceWith(process_tag(tag, valid_tags))

    result = soup.body.decode_contents()
    return re_clean_newlines.sub('\n', result).replace('\xa0', '&nbsp;')


@register.filter(is_safe=True)
def typograf(html):
    """
        Удаление висячих предлогов
    """
    soup = Soup(html, 'html5lib')
    for tag in soup.findAll(text=True):
        if re_nbsp.search(tag):
            new_tag = soup.new_string(unescape(re_nbsp.sub('\\1&nbsp;', tag)))
            tag.replace_with(new_tag)

    return soup.body.decode_contents().replace('\xa0', '&nbsp;')


@register.filter(is_safe=True, needs_autoescape=True)
def paragraphs(text, autoescape=True):
    """
        Разбивка текста на параграфы в местах переносов строк
    """
    text = re_clean_newlines.sub('\n', text)
    text = re_many_newlines.sub('\n', text)
    text_lines = text.strip().split('\n')

    if autoescape:
        text_lines = map(escape, text_lines)

    result = '<p>%s</p>' % '</p><p>'.join(text_lines)
    return mark_safe(result)


@register.filter(is_safe=True, needs_autoescape=True)
def lines(text, autoescape=True):
    """
        Разбивка текста на список по строкам
    """
    text = re_clean_newlines.sub('\n', text)
    text = re_many_newlines.sub('\n', text)
    text_lines = text.strip().split('\n')

    if autoescape:
        text_lines = map(escape, text_lines)

    result = '<li>%s</li>' % '</li><li>'.join(text_lines)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def clean(html, autoescape=None):
    """
        Алиас для трех фильтров: striptags, linebreaksbr, typograf, safe
    """
    text = strip_tags(str(html))
    text = defaultfilters.linebreaksbr(text, autoescape=autoescape)
    text = typograf(text)
    return mark_safe(text)


@register.filter(is_safe=True)
def softhyphen(value):
    """
        Вставка невидимых переносов в слова
    """
    cache = caches['default']
    language = settings.LANGUAGE_CODE

    key = ':'.join(map(str, (value, language)))
    if cache.has_key(key):
        return cache.get(key)
    else:
        result = hybernate_string(value)
        cache.set(key, result, timeout=6*3600)
        return result
