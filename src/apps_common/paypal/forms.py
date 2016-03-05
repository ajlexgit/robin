from hashlib import md5
from urllib.parse import urlencode
from django import forms
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from . import conf

# Типы действия
PAYPAL_TYPE_BUY = '_xclick'
PAYPAL_TYPE_DONATE = '_donations'
PAYPAL_TYPES = (
    (PAYPAL_TYPE_BUY, 'Buy form'),
    (PAYPAL_TYPE_DONATE, 'Donate form'),
)

FIELD_NAME_MAPPING = {
    'description': 'item_name',
    'result_url': 'notify_url',
    'success_url': 'return',
    'fail_url': 'cancel_return',
}


class BasePayPalForm(forms.Form):
    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)


class PayPalForm(BasePayPalForm):
    """ Форма для совершения платежа """
    # Параметр с URL'ом, на который будет отправлена форма.
    # Может пригодиться для использования в шаблоне.
    target = conf.FORM_TARGET

    # Тип действия
    cmd = forms.ChoiceField(choices=PAYPAL_TYPES, initial=PAYPAL_TYPE_BUY)

    # аккаунт магазина
    business = forms.CharField(max_length=128, initial=conf.EMAIL)

    # сумма к оплате
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # ID платежа
    invoice = forms.CharField(max_length=128)

    # описание покупки
    description = forms.CharField(max_length=128, required=False)

    # валюта оплаты
    currency_code = forms.CharField(max_length=8, initial=conf.CURRENCY)

    # кодировка
    charset = forms.CharField(max_length=8, initial='utf-8')

    # не требовать адрес
    no_shipping = forms.CharField(max_length=4, initial='1')

    rm = forms.CharField(max_length=4, initial='0')

    # адрес, обрабатывающий уведомления о платежах
    result_url = forms.URLField(max_length=1024)
    success_url = forms.URLField(max_length=1024)
    fail_url = forms.URLField(max_length=1024)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        self.initial['result_url'] = request.build_absolute_uri(resolve_url(conf.RESULT_URL))
        self.initial['success_url'] = request.build_absolute_uri(resolve_url(conf.SUCCESS_URL))
        self.initial['fail_url'] = request.build_absolute_uri(resolve_url(conf.FAIL_URL))

    def add_prefix(self, field_name):
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super().add_prefix(field_name)

    def get_redirect_url(self):
        """
            Получить URL с GET-параметрами, соответствующими значениям полей в
            форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
            ручной отправке формы методом GET.
        """
        params = {}
        for fieldname, field in self.fields.items():
            value = self._get_value(fieldname)
            if value:
                params[fieldname] = value

        return '{}?{}'.format(self.target, urlencode(params))


class PayPalResultForm(BasePayPalForm):
    """
        Форма для обработки результата оплаты
    """

    payment_status = forms.CharField(max_length=32)
    receiver_email = forms.EmailInput()
    invoice = forms.CharField(max_length=128)
    mc_gross = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
