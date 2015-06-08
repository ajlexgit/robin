from django.utils.translation import ugettext_lazy as _

def lj_description(**kwargs):
    url = kwargs.get('url')
    title = kwargs.get('title')
    image = kwargs.get('image')
    description = kwargs.get('description')
    
    result = ''
    if title:
        result += '<h1>%s</h1>\n' % title
    
    if image:
        result += '<img src="%s">\n' % image
    
    result += description + '\n'
    
    if url:
        result += '<a href="{0}" title>{0}</a>'.format(url)
    
    return result
    

SERVICES = {
    'vk': {
        'slug': 'vk',
        'title': _('VKontakte'),
        'endpoint': 'http://vk.com/share.php',
        'allowed_params': {
            'url': 'url',
            'title': 'title',
            'image': 'image',
            'description': 'description',
        },
    },
    'fb': {
        'slug': 'fb',
        'title': _('Facebook'),
        'endpoint': 'http://www.facebook.com/sharer.php',
        'allowed_params': {
            'url': 'u',
            'description': 't',
        },
    },
    'tw': {
        'slug': 'tw',
        'title': _('Twitter'),
        'endpoint': 'http://twitter.com/share',
        'allowed_params': {
            'url': 'url',
            'title': 'text',
        },
    },
    'gp': {
        'slug': 'gp',
        'title': _('Google Plus'),
        'endpoint': 'https://plus.google.com/share',
        'allowed_params': {
            'url': 'url',
        },
    },
    'lj': {
        'slug': 'lj',
        'title': _('Livejournal'),
        'endpoint': 'http://www.livejournal.com/update.bml',
        'allowed_params': {
            'title': 'subject',
            'description': 'event',
        },
        'modifiers': {
            'description': lj_description,
        }
    },
    'dg': {
        'slug': 'dg',
        'title': _('Digg'),
        'endpoint': 'http://digg.com/submit',
        'allowed_params': {
            'url': 'url',
            'title': 'title',
            'description': 'bodytext',
        },
    },
    'li': {
        'slug': 'li',
        'title': _('LinkedIn'),
        'endpoint': 'http://www.linkedin.com/shareArticle',
        'allowed_params': {
            'url': 'url',
        },
    },
    'pi': {
        'slug': 'pi',
        'title': _('Pin it'),
        'endpoint': 'http://www.pinterest.com/pin/create/button/',
        'allowed_params': {
            'url': 'url',
            'image': 'media',
            'description': 'description',
        },
    },
    'sb': {
        'slug': 'sb',
        'title': _('Surf it'),
        'endpoint': 'http://surfingbird.ru/share',
        'allowed_params': {
            'url': 'url',
            'title': 'title',
            'image': 'screenshot',
            'description': 'description',
        },
    },
}


