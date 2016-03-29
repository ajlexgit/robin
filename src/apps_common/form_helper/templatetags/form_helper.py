from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def render_form(context, form, template='form_helper/form.html'):
    return loader.get_template(template).render({
        'form': form,
    }, context.get('request'))


@register.simple_tag(takes_context=True)
def render_field(context, form, fieldname, template='form_helper/field.html', hidden_template='form_helper/hidden_field.html'):
    field = form[fieldname]
    if field.is_hidden:
        return loader.get_template(hidden_template).render({
            'field': field,
        }, context.get('request'))

    # классы поля
    classes = set()

    fieldclass_prefix = getattr(form, 'fieldclass_prefix', '')
    if fieldclass_prefix:
        classes.add('%s-%s' % (fieldclass_prefix, fieldname))
    else:
        classes.add(fieldname)

    if hasattr(form, 'get_field_fullname'):
        classes.add(form.get_field_fullname(fieldname))

    # ошибки поля
    field_errors = []
    if form.is_bound and fieldname in form.errors:
        invalid_class = getattr(form, 'invalid_class', None)
        if invalid_class:
            classes.add(invalid_class)

        if getattr(form, 'render_error_message', False):
            field_errors = field.errors

    return loader.get_template(template).render({
        'field': field,
        'field_classes': ' '.join(classes),
        'field_errors': field_errors,
    }, context.get('request'))
