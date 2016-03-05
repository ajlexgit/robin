from hashlib import md5
from urllib.parse import urlencode
from django import forms
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from . import conf


FIELD_NAME_MAPPING = {
    'first_name': 'x_first_name',
    'last_name': 'x_last_name',
    'company': 'x_company',
    'address': 'x_address',
    'city': 'x_city',
    'zip': 'x_zip',
    'country': 'x_country',
    'phone': 'x_phone',
    'email': 'x_email',
    'invoice': 'x_invoice_num',
    'description': 'x_description',
    'amount': 'x_amount',
    'result_url': 'x_relay_url',
}


class BaseGotobillingForm(forms.Form):
    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)


class GotobillingForm(BaseGotobillingForm):
    """ Форма для совершения платежа """
    # Параметр с URL'ом, на который будет отправлена форма.
    # Может пригодиться для использования в шаблоне.
    target = conf.FORM_TARGET

    # login магазина
    x_login = forms.CharField(max_length=8, initial=conf.LOGIN)

    x_show_form = forms.CharField(max_length=32, initial='PAYMENT_FORM')

    # имя плательщика
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    # название компании плательщика
    company = forms.CharField(max_length=50, required=False)

    # адрес плательщика
    address = forms.CharField(max_length=60, required=False)
    city = forms.CharField(max_length=40, required=False)
    state = forms.CharField(max_length=40, required=False)
    zip = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=60, required=False)

    # контакты плательщика
    phone = forms.CharField(max_length=25, required=False)
    email = forms.CharField(max_length=255, required=False)

    invoice = forms.CharField(max_length=20)
    description = forms.CharField(max_length=100, required=False)

    # сумма к оплате
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # Полный URL, куда перенаправляется пользователь после оплаты
    result_url = forms.URLField(max_length=255)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        self.initial['result_url'] = request.build_absolute_uri(resolve_url(conf.RESULT_URL))

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


class GotobillingResultForm(BaseGotobillingForm):
    """
        Форма для обработки результата оплаты
    """
    SIGNATURE_FIELDS = ('x_trans_id', 'x_amount')

    RESPONSE_CODE_APPROVED = '1'
    RESPONSE_CODE_DECLINED = '2'
    RESPONSE_CODE_ERROR = '3'
    RESPONSE_CODES = (
        (RESPONSE_CODE_APPROVED, _('Approved')),
        (RESPONSE_CODE_DECLINED, _('Declined')),
        (RESPONSE_CODE_ERROR, _('Error')),
    )

    x_response_code = forms.ChoiceField(choices=RESPONSE_CODES)
    x_response_reason_text = forms.CharField(max_length=255)
    x_type = forms.CharField(max_length=32)
    x_trans_id = forms.CharField(max_length=10)
    x_invoice_num = forms.CharField(max_length=20)
    x_amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    x_MD5_hash = forms.CharField(max_length=64)

    def calc_signature(self, hash_value=conf.HASH):
        hash_params = [hash_value, conf.LOGIN]
        for fieldname in self.SIGNATURE_FIELDS:
            value = self._get_value(fieldname)
            if value is None:
                value = ''
            hash_params.append(str(value))

        hash_data = ''.join(map(str, hash_params))
        hash_value = md5(hash_data.encode()).hexdigest().upper()
        return hash_value

    def clean(self):
        x_type = self.cleaned_data['x_type']
        if x_type != 'AUTH_CAPTURE':
            raise forms.ValidationError(_('Wrong transaction type: %s') % x_type)

        try:
            signature = self.cleaned_data['x_MD5_hash'].upper()
        except KeyError:
            raise forms.ValidationError(_('Undefined signature'))

        if signature != self.calc_signature():
            raise forms.ValidationError(_('Invalid signature'))

        return self.cleaned_data

