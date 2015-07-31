from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


REAL_FIELD_NAMES = {
    'short_dest': 'short-dest',
    'quickpay_form': 'quickpay-form',
    'need_fio': 'need-fio',
    'need_email': 'need-email',
    'need_phone': 'need-phone',
    'need_address': 'need-address',
}


class PaymentForm(forms.Form):
    TRANSACTION_TYPE = (
        ('shop', _('Shop')),
        ('donate', _('Donate')),
        ('small', _('Button')),
    )
    PAYMENT_TYPE = (
        ('PC', _('Yandex.Money')),
        ('AC', _('Payment card')),
    )
    BOOLEAN_CHOICES = (
        ('true', _('True')),
        ('false', _('False')),
    )


    receiver = forms.CharField(
        label=_('Reciever\'s wallet'),
        required=True,
        max_length=14,
        validators=[RegexValidator('^\d{14}$')],
    )
    formcomment = forms.CharField(
        label=_('Reciever\'s name'),
        required=True,
        max_length=50,
    )
    short_dest = forms.CharField(
        label=_('Payment name'),
        required=True,
        max_length=50,
    )
    quickpay_form = forms.ChoiceField(
        label=_('Transaction type'),
        required=True,
        initial='shop',
        choices=TRANSACTION_TYPE,
    )
    targets = forms.CharField(
        label=_('Payment target'),
        required=True,
        max_length=150,
    )
    sum = forms.DecimalField(
        label=_('Payment amount'),
        min_value=0,
        max_digits=7,
        decimal_places=2,
        required=True,
    )
    paymentType = forms.ChoiceField(
        label=_('Payment type'),
        required=True,
        choices=PAYMENT_TYPE,
        initial='PC',
    )

    label = forms.CharField(
        label=_('Label'),
        required=False,
        max_length=6,
    )
    comment = forms.CharField(
        label=_('Comment'),
        required=False,
        max_length=200,
        widget=forms.Textarea,
    )
    need_fio = forms.ChoiceField(
        label=_('Need full name'),
        required=False,
        choices=BOOLEAN_CHOICES,
        initial='false',
    )
    need_email = forms.ChoiceField(
        label=_('Need email'),
        required=False,
        choices=BOOLEAN_CHOICES,
        initial='false',
    )
    need_phone = forms.ChoiceField(
        label=_('Need phone'),
        required=False,
        choices=BOOLEAN_CHOICES,
        initial='false',
    )
    need_address = forms.ChoiceField(
        label=_('Need address'),
        required=False,
        choices=BOOLEAN_CHOICES,
        initial='false',
    )

    def clean(self):
        formcomment = self.cleaned_data.get('formcomment')
        short_dest = self.cleaned_data.get('short_dest')

        # formcomment должен быть равен short_dest
        if formcomment is not None and short_dest is not None:
            if formcomment != short_dest:
                self.add_error('short_dest', _('Payment name should be queal'))

        return super().clean()

    def add_prefix(self, field_name):
        """ Замена имен полей формы """
        field_name = REAL_FIELD_NAMES.get(field_name, field_name)
        return field_name