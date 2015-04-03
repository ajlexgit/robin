from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def js_storage_out(context):
    return '<script type="text/javascript">{0}</script>'.format(
        context['request'].js_storage.out()
    )
