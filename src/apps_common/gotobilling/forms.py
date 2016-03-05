from hashlib import md5
from urllib.parse import urlencode
from django import forms
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from . import conf


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
    x_first_name = forms.CharField(max_length=50, required=False)
    x_last_name = forms.CharField(max_length=50, required=False)

    # название компании плательщика
    x_company = forms.CharField(max_length=50, required=False)

    # адрес плательщика
    x_address = forms.CharField(max_length=60, required=False)
    x_city = forms.CharField(max_length=40, required=False)
    x_state = forms.CharField(max_length=40, required=False)
    x_zip = forms.CharField(max_length=20, required=False)
    x_country = forms.CharField(max_length=60, required=False)

    # контакты плательщика
    x_phone = forms.CharField(max_length=25, required=False)
    x_email = forms.CharField(max_length=255, required=False)

    x_invoice_num = forms.CharField(max_length=20, required=False)
    x_description = forms.CharField(max_length=100, required=False)

    # сумма к оплате
    x_amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # Полный URL, куда перенаправляется пользователь после оплаты
    x_relay_url = forms.URLField(max_length=255)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        self.initial['x_relay_url'] = request.build_absolute_uri(resolve_url(conf.RELAY_URL))

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

