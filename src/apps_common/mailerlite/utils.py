from bs4 import BeautifulSoup as Soup
from django.contrib.sites.shortcuts import get_current_site


def format_html(html, scheme='//'):
    """
        1. Все ссылки становятся абсолютными с target=_blank.
        2. Ко всем таблицам добавляются аттрибуты cellpadding, cellspacing и border
    """
    site = get_current_site(None)

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