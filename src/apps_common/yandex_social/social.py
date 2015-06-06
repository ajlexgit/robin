import random
import string
from django.conf import settings
from django.template import loader

DEFAULT_BUTTONS = getattr(settings, 'SOCIAL_BUTTONS_DEFAULT', ('vkontakte', 'facebook', 'twitter', 'gplus'))
DEFAULT_BUTTON_TYPE = getattr(settings, 'SOCIAL_BUTTON_TYPE_DEFAULT', 'default')
DEFAULT_BUTTON_THEME = getattr(settings, 'SOCIAL_BUTTON_THEME_DEFAULT', 'counter')


def social_buttons(options, buttons=DEFAULT_BUTTONS, button_type=DEFAULT_BUTTON_TYPE,
                   theme=DEFAULT_BUTTON_THEME):
    if not options.get('url'):
        raise ValueError('url is required')
    elif not options.get('title'):
        raise ValueError('title is required')
    elif not options.get('description'):
        raise ValueError('description is required')

    options = {key: str(value).strip() for key, value in options.items()}

    rand_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return loader.render_to_string('social/social.html', dict(options, **{
        'id': rand_id,
        'buttons': ','.join(buttons),
        'type': button_type,
        'theme': theme,
    }))
