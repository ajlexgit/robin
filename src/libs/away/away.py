from urllib import parse
from bs4 import BeautifulSoup as Soup
from django.shortcuts import resolve_url
from django.contrib.sites.shortcuts import get_current_site


def is_same_domain(host, pattern):
    if not pattern:
        return False

    pattern = pattern.lower()
    return (
        pattern[0] == '.' and (host.endswith(pattern) or host == pattern[1:]) or
        pattern == host
    )


def away_links(request, html):
    """
        Заменяет все внешние ссылки в html-коде на единую точку с редиректом
    """
    site = get_current_site(request)
    soup = Soup(html, 'html5lib')
    for tag in soup.findAll('a'):
        if tag.get('href'):
            parsed = parse.urlparse(tag['href'])
            if '' not in (parsed.scheme, parsed.netloc) and not parsed.query and not is_same_domain(parsed.netloc, site.domain):
                tag['target'] = '_blank'
                tag['href'] = resolve_url('away') + '?url=' + parsed.geturl()
                tag.string = parse.unquote(tag.string)

    return soup.body.decode_contents()
