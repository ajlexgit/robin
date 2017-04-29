import hmac
import time
from hashlib import md5
from urllib.parse import urlencode
from django import forms
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from . import conf

FIELD_NAME_MAPPING = {
    'amount': 'x_amount',
    'first_name': 'x_first_name',
    'last_name': 'x_last_name',
    'company': 'x_company',
    'address': 'x_address',
    'city': 'x_city',
    'state': 'x_state',
    'zip': 'x_zip',
    'country': 'x_country',
    'phone': 'x_phone',
    'email': 'x_email',
    'invoice': 'x_invoice_num',
    'description': 'x_description',
}


class BaseAuthorizeNetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '')
        super().__init__(*args, **kwargs)

    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)


class PaymentForm(BaseAuthorizeNetForm):
    """ Форма для совершения платежа """

    # Параметр с URL'ом, на который будет отправлена форма.
    # Может пригодиться для использования в шаблоне.
    target = conf.FORM_TARGET

    # Обязательные поля. Не имеет отношения к валидации формы.
    # Перечисляются поля, в которых должно быть заполнено
    # начальное значение при создании формы
    REQUIRE_INITIAL = ('invoice', 'amount')

    x_login = forms.CharField(max_length=20, initial=conf.LOGIN_ID)
    x_fp_sequence = forms.CharField(max_length=128, initial=conf.SEQUENCE)
    x_show_form = forms.CharField(max_length=32, initial='PAYMENT_FORM')
    x_version = forms.CharField(max_length=3, initial='3.1')

    x_fp_timestamp = forms.IntegerField()
    x_fp_hash = forms.CharField(max_length=64)

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
    description = forms.CharField(max_length=255, required=False)

    # сумма к оплате
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # Полный URL, куда перенаправляется пользователь при отмене платежа
    x_cancel_url = forms.URLField(max_length=255)

    x_receipt_link_method = forms.CharField(max_length=5, required=False)
    x_receipt_link_text = forms.CharField(max_length=50, required=False)
    x_receipt_link_URL = forms.URLField(max_length=255, required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_url(request, 'x_cancel_url', conf.CANCEL_URL)

        if conf.RECEIPT_URL:
            self.initial['x_receipt_link_method'] = 'LINK'
            self.initial['x_receipt_link_text'] = _('Click here to return to the merchant site')
            self._initial_url(request, 'x_receipt_link_URL', conf.RECEIPT_URL)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        if conf.TEST_MODE:
            self.fields['x_test_request'] = forms.CharField(
                required=False,
                initial='TRUE',
                widget=forms.HiddenInput,
            )

        for fieldname in self.REQUIRE_INITIAL:
            value = self.initial.get(fieldname)
            if not value:
                raise ValueError('"%s" field requires initial value' % fieldname)

        self.initial['x_fp_timestamp'] = int(time.time())
        self.initial['x_fp_hash'] = self.calc_signature()

    def add_prefix(self, field_name):
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super().add_prefix(field_name)

    def _initial_url(self, request, fieldname, default):
        """
            Добавление initial-значения в поле fieldname, которое является полной ссылкой
            на страницу
        """
        url = self.initial.get(fieldname, '')
        if url:
            if not url.startswith('http'):
                self.initial[fieldname] = request.build_absolute_uri(resolve_url(url))
            return

        self.initial[fieldname] = request.build_absolute_uri(resolve_url(default))

    def calc_signature(self):
        hash_str = '^'.join(map(str, (
            self._get_value('x_login'),
            self._get_value('x_fp_sequence'),
            self._get_value('x_fp_timestamp'),
            self._get_value('amount'),
            '',
        )))
        hasher = hmac.new(conf.TRANSACTION_KEY.encode(), hash_str.encode(), digestmod=md5)
        return hasher.hexdigest()

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
                real_fieldname = FIELD_NAME_MAPPING.get(fieldname, fieldname)
                params[real_fieldname] = value

        return '{}?{}'.format(self.target, urlencode(params))


class AuthorizeNetResultForm(BaseAuthorizeNetForm):
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
    x_trans_id = forms.CharField(max_length=20, required=False)
    x_invoice_num = forms.CharField(max_length=20)
    x_amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    x_MD5_Hash = forms.CharField(max_length=64, required=False)

    def calc_signature(self):
        hash_params = [conf.MD5_HASH, conf.LOGIN_ID]
        for fieldname in self.SIGNATURE_FIELDS:
            value = self._get_value(fieldname)
            if value is None:
                hash_params.append('')
            elif fieldname == 'x_amount':
                # Force decimal places
                hash_params.append('%.2f' % value)
            else:
                hash_params.append(str(value))

        hash_data = ''.join(map(str, hash_params))
        hash_value = md5(hash_data.encode()).hexdigest().upper()
        return hash_value

    def clean(self):
        try:
            x_type = self.cleaned_data['x_type'].upper()
        except KeyError:
            raise forms.ValidationError(_('Undefined signature'))
        else:
            if x_type != 'AUTH_CAPTURE':
                raise forms.ValidationError(_('Wrong transaction type: %s') % x_type)

        try:
            signature = self.cleaned_data['x_MD5_Hash'].upper()
        except KeyError:
            raise forms.ValidationError(_('Undefined signature'))

        if signature != self.calc_signature():
            raise forms.ValidationError(_('Invalid signature'))

        return self.cleaned_data

