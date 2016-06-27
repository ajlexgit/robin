import re
from bs4 import BeautifulSoup as Soup
from django.template import Library
from django.contrib.sites.shortcuts import get_current_site

register = Library()
re_http = re.compile(r'^https?://', re.IGNORECASE)


@register.simple_tag(takes_context=True)
def absolute_links(context, html, scheme=None):
    """
        Все ссылки становятся абсолютными с target=_blank
    """
    request = context.get('request')
    site = get_current_site(request)
    scheme = scheme or (request and request.scheme) or 'http'

    soup = Soup(html, 'html5lib')
    for tag in soup.findAll('a'):
        href = tag.get('href')
        if not href:
            continue

        tag['target'] = '_blank'
        if href.startswith('//'):
            tag['href'] = '%s:%s' % (scheme, href)
        elif not re_http.match(href):
            tag['href'] = '%s://%s%s' % (scheme, site.domain, href)

    for tag in soup.findAll('img'):
        src = tag.get('src')
        if not src:
            continue

        if src.startswith('//'):
            tag['src'] = '%s:%s' % (scheme, src)
        elif not re_http.match(src):
            tag['src'] = '%s://%s%s' % (scheme, site.domain, src)

        # srcset
        srcset = tag.get('srcset')
        if not srcset:
            continue

        srcset_final = []
        for srcset_part in srcset.split(','):
            url, width = srcset_part.strip().split()
            if url.startswith('//'):
                url = '%s:%s' % (scheme, url)
            elif not re_http.match(url):
                url = '%s://%s%s' % (scheme, site.domain, url)
            srcset_final.append('%s %s' % (url, width))
        tag['srcset'] = ','.join(srcset_final)

    return soup.body.decode_contents()