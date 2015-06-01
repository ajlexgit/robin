import re
from bs4 import BeautifulSoup as Soup, NavigableString
from django.utils.html import strip_tags


def strip_tags_except(html, valid_tags=()):
    """ Удаление HTML-тэгов, кроме перечисленных в valid_tags """
    soup = Soup(html)
    body = soup.body.contents if soup.body else soup
    for tag in body:
        if isinstance(tag, NavigableString):
            continue

        if tag.name in valid_tags:
            for c in tag.contents:
                if isinstance(c, NavigableString) and not c.strip():
                    c.replaceWith('')
            continue

        s = ""
        for c in tag.contents:
            if not isinstance(c, NavigableString):
                c = strip_tags_except(str(c), valid_tags)
            s += str(c)

        tag.replaceWith(s)

    body = soup.body.contents if soup.body else soup
    text = '\n'.join(str(tag) for tag in body)
    return re.sub('\n([ \r\t\xa0]*\n)+', '\n', text.strip())


def _collect_lines(lines, maxlen):
    """
        Выборка первых строк из последовательности lines,
        чтобы суммарная длина не превышала maxlen.
        Возвращает кортеж, состоящий из из:
            список подхоящих строк
            список остальных строк
            суммарную длину подходящих строк
    """
    result_lines = []
    result_len = 0
    for line in lines:
        # Игнорируем тэги при подсчете длины
        line_len = len(strip_tags(line))
        if result_len + line_len <= maxlen:
            result_lines.append(line)
            result_len += line_len
        else:
            break

    return result_lines, lines[len(result_lines):], result_len


def description(text, minlen, maxlen):
    """
        Собираем параграфы до достижения заданной длины.
        Если недобрали - добираем предложениями из следующего параграфа.

        Принимает текст, разделенный на параграфы символом перевода строки.
    """
    paragraphs, other_paragraphs, paragraphs_len = _collect_lines(text.split('\n'), maxlen)
    if other_paragraphs and paragraphs_len < minlen:
        lines, other_lines, lines_len =  _collect_lines(other_paragraphs[0].split('. '), maxlen - paragraphs_len)
        if lines:
            paragraphs.append('. '.join(lines) + '.')
        else:
            # Первое предложение следующего параграфа слишком длинное
            if paragraphs:
                # Если уже что-то набрали параграфами - добавляем многоточие
                last_line = paragraphs[-1].rstrip()
                if last_line[-1] == '.':
                    last_line = last_line[:-1] + '...'
                else:
                    last_line += '...'
                paragraphs[-1] = last_line
            elif other_lines:
                # Вообще текст набрать не удалось. Набираем по словам из первого предложения + многоточие
                words, other_words, words_len = _collect_lines(other_lines[0].split(' '), maxlen)
                paragraphs.append(' '.join(words) + '...')

    paragraphs = list(map(str.strip, paragraphs))
    paragraphs = list(filter(bool, paragraphs))
    return '\n'.join(paragraphs)
