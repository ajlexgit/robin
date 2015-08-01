from django.template import Library, loader
from ..forms import PaymentForm
from .. import options

register = Library()


@register.simple_tag
def yandex_money_url():
    return options.PAYMENT_URL


@register.simple_tag
def yandex_money(amount, payment_type='AC', label='', description='', targets=''):
    try:
        float(amount)
    except (TypeError, ValueError):
        raise ValueError('invalid payment amount')

    if not payment_type in dict(PaymentForm.PAYMENT_TYPE):
        raise ValueError('invalid payment type')

    description = description or options.DEFAULT_DESCRIPTION
    if not description:
        raise ValueError('empty payment description')

    targets = targets or options.DEFAULT_TARGETS
    if not targets:
        raise ValueError('empty payment targets')

    form = PaymentForm(initial={
        'receiver': options.WALLET,
        'formcomment': description,
        'short_dest': description,
        'targets': targets,
        'sum': amount,
        'paymentType': payment_type,

        'label': label,
    })

    return loader.render_to_string('yandex_money/form.html', {
        'form': form,
    })