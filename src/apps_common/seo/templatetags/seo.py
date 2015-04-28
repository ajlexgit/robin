from django.template import loader, Library
from django.contrib.contenttypes.models import ContentType
from ..models import SeoText

register = Library()


@register.simple_tag
def seo_block(instance, template='seo/block.html'):
    content_type = ContentType.objects.get_for_model(type(instance))
    try:
        seo = SeoText.objects.get(
            content_type=content_type,
            object_id=instance.pk,
        )
    except (SeoText.DoesNotExist, SeoText.MultipleObjectsReturned):
        return ''

    return loader.render_to_string(template, {
        'seo': seo,
    })