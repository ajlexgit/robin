import re
from bs4 import BeautifulSoup as Soup
from django.conf import settings
from django.template import loader
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags

re_newline_spaces = re.compile(r'[\r \t]*\n[\r \t]*')
re_newlines = re.compile(r'\n{3,}')


def send(request, receivers, subject, message, fail_silently=True):
    if not receivers:
        return True
    if isinstance(receivers, str):
        receivers = [receivers]

    # Вставка домена в subject
    site = get_current_site(request)
    subject = subject.format(domain=site.domain)

    plain = strip_tags(message)
    plain = re_newline_spaces.sub('\n', plain)
    plain = re_newlines.sub('\n\n', plain)

    send_mail(
        subject=subject,
        message=plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=receivers,
        html_message=message,
        fail_silently=fail_silently,
    )


def send_template(request, receivers, subject, template, context=None, fail_silently=True):
    # Добавляем в контекст текущий домен
    site = get_current_site(request)
    context['domain'] = site.domain
    message = loader.get_template(template).render(context, request)
    send(request, receivers, subject, message, fail_silently=fail_silently)


def absolute_links(html, scheme='//', request=None):
    """
        1. Все ссылки становятся абсолютными с target=_blank.
        2. Ко всем таблицам добавляются аттрибуты cellpadding, cellspacing и border
    """
    site = get_current_site(request)

    soup = Soup(html, 'html5lib')
    for tag in soup.findAll('a'):
        href = tag.get('href')
        if not href:
            continue

        tag['target'] = '_blank'
        if href.startswith('//'):
            tag['href'] = '%s%s' % (scheme, href[2:])
        elif href.startswith('/'):
            tag['href'] = '%s%s%s' % (scheme, site.domain, href)

    for tag in soup.findAll('img'):
        if tag.has_attr('height'):
            del tag['height']

        src = tag.get('src')
        if not src:
            continue

        if src.startswith('//'):
            tag['src'] = '%s%s' % (scheme, src[2:])
        elif src.startswith('/'):
            tag['src'] = '%s%s%s' % (scheme, site.domain, src)

        # srcset
        srcset = tag.get('srcset')
        if not srcset:
            continue

        srcset_final = []
        for srcset_part in srcset.split(','):
            url, width = srcset_part.strip().split()
            if url.startswith('//'):
                url = '%s%s' % (scheme, url[2:])
            elif src.startswith('/'):
                url = '%s%s%s' % (scheme, site.domain, url)
            srcset_final.append('%s %s' % (url, width))
        tag['srcset'] = ','.join(srcset_final)

    # Добавление аттрибутов к таблицам
    for tag in soup.findAll('table'):
        for attr in ('border', 'cellpadding', 'cellspacing'):
            if not tag.has_attr(attr):
                tag[attr] = '0'

    return soup.decode_contents()
