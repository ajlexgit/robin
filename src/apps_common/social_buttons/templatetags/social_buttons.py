from urllib.parse import urlencode
from django.template import loader, Library

register = Library()


@register.simple_tag(takes_context=True)
def social_button(context, provider, text=None, url=None, title=None, description=None, image=None):
    request = context.get('request')
    if not request:
        return ''

    social_data = {
        'url': url,
        'title': title,
        'description': description,
        'image': image,
    }

    og = getattr(request, 'opengraph', None)
    if og is not None:
        social_data.update(og.data)

    provider = provider.lower()
    if provider == 'vk':
        share_url = 'http://vk.com/share.php?%s' % urlencode(social_data)
    elif provider == 'fb':
        share_url = 'http://www.facebook.com/sharer/sharer.php?u=%s' % social_data['url']
    elif provider == 'tw':
        share_url = 'http://twitter.com/share?url=%s&text=%s' % (social_data['url'], social_data.get('description'))
    elif provider == 'gp':
        share_url = 'https://plus.google.com/share?url=%s' % social_data['url']
    elif provider == 'li':
        social_data = {
            'mini': 'true',
            'url': social_data['url'],
            'title': social_data.get('title'),
            'image': social_data.get('image'),
            'summary': social_data.get('description'),
        }
        share_url = 'http://www.linkedin.com/shareArticle?%s' % urlencode(social_data)
    elif provider == 'pn':
        social_data = {
            'url': social_data['url'],
            'media': social_data.get('image'),
            'description': social_data.get('description'),
        }
        share_url = 'http://www.pinterest.com/pin/create/button/?%s' % urlencode(social_data)
    else:
        return ''

    return loader.render_to_string('social_buttons/button.html', {
        'share_url': share_url,
        'provider': provider,
        'text': text,
    }, request=request)
