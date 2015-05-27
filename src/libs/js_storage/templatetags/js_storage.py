from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def js_storage_out(context):
    request = context.get('request')
    if not request:
        return ''

    return '<script type="text/javascript">{0}</script>'.format(
        request.js_storage.out()
    )
