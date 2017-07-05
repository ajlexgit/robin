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
def render_field(context, form, fieldname, template=None, classes=None, **kwargs):
    """
        Рендеринг одного поля формы.

        Пример:
            {% render_field form 'name' classes='blue-field big-field' %}
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
    if classes is not None:
        classes = {classname.strip() for classname in classes.split(' ')}
    else:
        classes = set()

    fieldclass_prefix = getattr(form, 'fieldclass_prefix', 'field')
    if fieldclass_prefix:
        classes.add('%s-%s' % (fieldclass_prefix, fieldname))
    else:
        classes.add(fieldname)

    if hasattr(form, 'get_field_fullname'):
        classes.add(form.get_field_fullname(fieldname))

    if field.field.required:
        required_css_class = getattr(form, 'required_css_class', 'required')
        if required_css_class:
            classes.add(required_css_class)

    # классы для неверно заполненного поля
    field_errors = []
    if form.is_bound and form._errors and fieldname in form._errors:
        invalid_css_class = getattr(form, 'invalid_css_class', 'invalid')
        if invalid_css_class:
            classes.add(invalid_css_class)

        if getattr(form, 'render_error_message', False):
            field_errors = field.errors

    template = template or get_field_template(form, field)
    context = dict({
        'form': form,
        'field': field,
        'field_classes': ' '.join(classes),
        'field_errors': field_errors,
    }, **kwargs)
    return loader.get_template(template).render(context, request)
