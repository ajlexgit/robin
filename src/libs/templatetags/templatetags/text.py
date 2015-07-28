import re
from html import unescape
from softhyphen.html import get_hyphenator_for_language, SOFT_HYPHEN
from bs4 import BeautifulSoup as Soup, NavigableString
from django.conf import settings
from django.core.cache import caches
from django.template import Library, defaultfilters
from django.utils.html import strip_tags

register = Library()

re_nbsp = re.compile('\\b([\'\"\.\w]{1,3})\s+')
re_clean_newlines = re.compile('[ \r\t\xa0]*\n')
re_many_newlines = re.compile('\n{2,}')


@register.filter(is_safe=True, name="striptags_except")
def strip_tags_except_filter(html, args):
    """
        Удаление HTML-тэгов, кроме перечисленных в valid_tags.

        Пример:
            {{ text|striptags_except:"a, p" }}
    """
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

    valid_tags = [item.strip() for item in args.split(',')]

    soup = Soup(html, 'html5lib')

    for tag in soup.body:
        tag.replaceWith(process_tag(tag))

    result = soup.body.decode_contents()
    return re_clean_newlines.sub('\n', result)


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

    return soup.body.decode_contents()


@register.filter(is_safe=True)
def paragraphs(text):
    """
        Разбивка текста на параграфы в местах переносов строк
    """
    text = re_clean_newlines.sub('\n', text)
    text = re_many_newlines.sub('\n', text)
    result = '<p>%s</p>' % '</p><p>'.join(text.strip().split('\n'))
    return result


@register.filter(is_safe=True, needs_autoescape=True)
def clean(html, autoescape=None):
    """
        Алиас для трех фильтров: striptags, linebreaksbr, typograf
    """
    text = strip_tags(html)
    text = defaultfilters.linebreaksbr(text, autoescape=autoescape)
    text = typograf(text)
    return text


@register.simple_tag(takes_context=True)
def softhyphen(context, value, language=None):
    request = context.get('request')
    if not request:
        return value

    if not language:
        language = settings.LANGUAGE_CODE

    cache = caches['default']
    key = ':'.join((value, language))
    if cache.has_key(key):
        return cache.get(key)
    else:
        hybernator = get_hyphenator_for_language(language)
        result = hybernator.inserted(value, SOFT_HYPHEN)
        cache.set(key, result, timeout=24 * 3600)
        return result
