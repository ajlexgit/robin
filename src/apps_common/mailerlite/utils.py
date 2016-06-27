from bs4 import BeautifulSoup as Soup
from django.contrib.sites.shortcuts import get_current_site


def absolute_links(html, scheme='//'):
    """
        Все ссылки становятся абсолютными с target=_blank
    """
    site = get_current_site(None)

    soup = Soup('<body>%s</body>' % html, 'html5lib')
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
        src = tag.get('src')
        if not src:
            continue

        if src.startswith('//'):
            tag['src'] = '%s%s' % (scheme, src[2:])
        elif href.startswith('/'):
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
            elif href.startswith('/'):
                url = '%s%s%s' % (scheme, site.domain, url)
            srcset_final.append('%s %s' % (url, width))
        tag['srcset'] = ','.join(srcset_final)

    return soup.body.decode_contents()