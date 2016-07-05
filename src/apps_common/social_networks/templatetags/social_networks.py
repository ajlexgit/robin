from urllib.parse import urlencode
from collections import defaultdict
from django.template import loader, Library

register = Library()


@register.simple_tag(takes_context=True)
def social_button(context, provider, text='', url='', title='', description='', image=''):
    request = context.get('request')
    if not request:
        return ''

    social_data = defaultdict(lambda: '')

    # Берем данные из Opengraph
    seo = getattr(request, 'seo', None)
    if seo is not None:
        opengraph = seo['opengraph']
        social_data.update(opengraph._dict)

    # Возможность переопределения
    if url:
        social_data['url'] = url
    if title:
        social_data['title'] = title
    if description:
        social_data['description'] = description
    if image:
        social_data['image'] = image

    # Построение URL для расшаривания
    provider = provider.lower()
    if provider == 'vk':
        social_data = {
            'url': social_data['url'],
            'title': social_data['title'],
            'image': social_data['image'],
            'description': social_data['description'],
        }
        share_url = 'http://vk.com/share.php?%s' % urlencode(social_data)
    elif provider == 'fb':
        social_data = {
            'u': social_data['url'],
        }
        share_url = 'http://www.facebook.com/sharer/sharer.php?%s' % urlencode(social_data)
    elif provider == 'tw':
        social_data = {
            'url': social_data['url'],
            'text': social_data['description'],
        }
        share_url = 'http://twitter.com/share?%s' % urlencode(social_data)
    elif provider == 'gp':
        social_data = {
            'url': social_data['url'],
        }
        share_url = 'https://plus.google.com/share?%s' % urlencode(social_data)
    elif provider == 'li':
        social_data = {
            'mini': 'true',
            'url': social_data['url'],
            'title': social_data['title'],
            'image': social_data['image'],
            'summary': social_data['description'],
        }
        share_url = 'http://www.linkedin.com/shareArticle?%s' % urlencode(social_data)
    elif provider == 'pn':
        social_data = {
            'url': social_data['url'],
            'media': social_data['image'],
            'description': social_data['description'],
        }
        share_url = 'http://www.pinterest.com/pin/create/button/?%s' % urlencode(social_data)
    else:
        return ''

    return loader.render_to_string('social_networks/button.html', {
        'share_url': share_url,
        'provider': provider,
        'text': text,
    }, request=request)
