from urllib import parse
from bs4 import BeautifulSoup as Soup
from django.shortcuts import resolve_url
from django.contrib.sites.shortcuts import get_current_site


def same_domain(domain1, domain2):
    parts1 = domain1.split('.')
    parts2 = domain2.split('.')
    return parts1[-2:] == parts2[-2:]


def away_links(request, html, target="_blank"):
    """
        Заменяет все внешние ссылки в html-коде на единую точку с редиректом
    """
    site = get_current_site(request)
    soup = Soup(html)
    for tag in soup.findAll('a'):
        tag['target'] = target
        parsed = parse.urlparse(tag['href'])
        if parsed.netloc and not same_domain(parsed.netloc, site.domain):
            tag['href'] = resolve_url('away') + '?url=' + parsed.geturl()
            tag.string = parse.unquote(tag.string)

    body = soup.body.contents if soup.body else soup
    text = '\n'.join(str(tag) for tag in body)
    return text.strip()
