from django.conf import settings
from django.template import loader, Library
from django.template.context import RequestContext
from .. import options

register = Library()


@register.simple_tag(takes_context=True)
def select_language(context, current_code=None):
    request = context.get('request')
    if not request:
        return ''

    if not current_code or not current_code in options.LANGUAGE_CODES:
        current_code = settings.LANGUAGE_CODE

    other_langs = tuple(item for item in options.LANGUAGES if item['code'] != current_code)

    return loader.render_to_string('multilanguage/allowed_languages.html', RequestContext(request, {
        'current_code': current_code,
        'langs': other_langs,
    }))
