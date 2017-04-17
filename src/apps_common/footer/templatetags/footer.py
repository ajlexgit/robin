import binascii
from django.template import Library, loader
from django.contrib.sites.shortcuts import get_current_site
from .. import conf

register = Library()


@register.simple_tag(takes_context=True)
def footer(context, template='footer/footer.html'):
    """ Футер """
    return loader.render_to_string(template, {

    }, request=context.get('request'))


@register.simple_tag(takes_context=True)
def dl_link(context, template='footer/dl_link.html'):
    request = context.get('request')
    if not request:
        return ''

    site = get_current_site(request)
    website = site.domain
    page_info = request.path_info

    set_crc = binascii.crc32(('set:%s:%s' % (website, page_info)).encode())
    set_names = tuple(sorted(conf.DL_LINKS.keys()))
    url_set = conf.DL_LINKS[set_names[set_crc % len(set_names)]]

    url_crc = binascii.crc32(('url:%s:%s' % (website, page_info)).encode())
    records = tuple(sorted(url_set, key=lambda x: x['url']))
    record = records[url_crc % len(url_set)]

    return loader.render_to_string(template, record, request=context.get('request'))
