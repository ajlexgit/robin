from django.template import loader, RequestContext
from .models import SocialConfig


def follow_us_render(request, block):
    config = SocialConfig.get_solo()
    if not config.facebook and not config.twitter and not config.youtube:
        return ''

    context = RequestContext(request, {
        'config': config,
        'block': block,
    })
    return loader.render_to_string('social/follow_us.html', context_instance=context)
