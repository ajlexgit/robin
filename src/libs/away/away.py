from urllib import parse
from bs4 import BeautifulSoup as Soup
from django.shortcuts import resolve_url
from django.contrib.sites.shortcuts import get_current_site


def is_same_domain(domain1, domain2):
    parts1 = domain1.split('.')
    parts2 = domain2.split('.')
    return parts1[-2:] == parts2[-2:]


def away_links(request, html, target="_blank"):
    """
        Заменяет все внешние ссылки в html-коде на единую точку с редиректом
    """
    site = get_current_site(request)
    soup = Soup(html, 'html5lib')
    for tag in soup.findAll('a'):
        if tag.get('href'):
            tag['target'] = target
            parsed = parse.urlparse(tag['href'])
            if parsed.netloc and not is_same_domain(parsed.netloc, site.domain):
                tag['href'] = resolve_url('away') + '?url=' + parsed.geturl()
                tag.string = parse.unquote(tag.string)

    return soup.body.decode_contents()
