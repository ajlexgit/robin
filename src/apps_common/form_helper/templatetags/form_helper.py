from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def render_form(context, form, template=None):
    """
        Рендеринг формы.

        Пример:
            {% render_form form %}
    """
    template = template or 'form_helper/form.html'
    return loader.get_template(template).render({
        'form': form,
    }, context.get('request'))


def get_field_template(form, field):
    """
        Определние шаблона для рендеринга поля
    """
    template_overrides = getattr(form, 'field_templates', None)
    if template_overrides and field.name in template_overrides:
        return template_overrides[field.name]

    if field.is_hidden:
        return getattr(form, 'hidden_field_template', 'form_helper/hidden_field.html')
    else:
        return getattr(form, 'field_template', 'form_helper/field.html')


@register.simple_tag(takes_context=True)
def render_field(context, form, fieldname, template=None):
    """
        Рендеринг одного поля формы.

        Пример:
            {% render_field form 'name' %}
    """
    request = context.get('request')
    if not request:
        return ''

    field = form[fieldname]
    if field.is_hidden:
        template = template or get_field_template(form, field)
        return loader.get_template(template).render({
            'field': field,
        }, request)

    # классы поля
    classes = set()
    fieldclass_prefix = getattr(form, 'fieldclass_prefix', 'field')
    if fieldclass_prefix:
        classes.add('%s-%s' % (fieldclass_prefix, fieldname))
    else:
        classes.add(fieldname)

    if hasattr(form, 'get_field_fullname'):
        classes.add(form.get_field_fullname(fieldname))

    # классы для неверно заполненного поля
    field_errors = []
    if form.is_bound and fieldname in form.errors:
        invalid_class = getattr(form, 'invalid_class', 'invalid')
        if invalid_class:
            classes.add(invalid_class)

        if getattr(form, 'render_error_message', False):
            field_errors = field.errors

    template = template or get_field_template(form, field)
    return loader.get_template(template).render({
        'form': form,
        'field': field,
        'field_classes': ' '.join(classes),
        'field_errors': field_errors,
    }, request)
