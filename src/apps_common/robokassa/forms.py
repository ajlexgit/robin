from hashlib import md5
from urllib.parse import urlencode, quote_plus
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import conf


class BaseRobokassaForm(forms.Form):
    SIGNATURE_FIELDS = ('MrchLogin', 'OutSum', 'InvId')
    PASSWD = conf.PASSWORD1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # создаем дополнительные поля
        for key in conf.EXTRA_PARAMS:
            self.fields[key] = forms.CharField(required=False)
            if 'initial' in kwargs:
                self.fields[key].initial = kwargs['initial'].get(key, None)

    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)

    def calc_signature(self):
        hash_params = []
        for fieldname in self.SIGNATURE_FIELDS:
            value = self._get_value(fieldname)
            if value is None:
                value = ''
            hash_params.append(str(value))

        hash_params.append(self.PASSWD)

        # extra
        for key in sorted(conf.EXTRA_PARAMS):
            value = self._get_value(key)
            if value is None:
                value = ''
            value = quote_plus(str(value))
            hash_params.append('%s=%s' % (key, value))

        hash_data = ':'.join(map(str, hash_params))
        hash_value = md5(hash_data.encode()).hexdigest().upper()
        return hash_value


class RobokassaForm(BaseRobokassaForm):
    """ Форма для совершения платежа """
    # Параметр с URL'ом, на который будет отправлена форма.
    # Может пригодиться для использования в шаблоне.
    target = conf.FORM_TARGET

    # login магазина в обменном пункте
    MrchLogin = forms.CharField(max_length=20, initial=conf.LOGIN)

    # сумма к оплате
    OutSum = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # описание покупки. Эта информация отображается в интерфейсе ROBOKASSA и в Электронной квитанции
    Desc = forms.CharField(max_length=100)

    # контрольная сумма MD5
    SignatureValue = forms.CharField(max_length=32)

    # Номер счета в магазине. Значение этого параметра должно быть уникальным для каждой оплаты
    InvId = forms.IntegerField(min_value=0)

    # Кодировка, в которой отображается страница ROBOKASSA.
    Encoding = forms.CharField(max_length=16, initial='utf-8')

    # Предлагаемый способ оплаты. Тот вариант оплаты, который Вы рекомендуете использовать своим покупателям.
    # https://merchant.roboxchange.com/WebService/Service.asmx/GetCurrencies?MerchantLogin=demo&language=ru
    IncCurrLabel = forms.CharField(max_length=32, required=False)

    # e-mail пользователя
    Email = forms.EmailField(required=False)

    # язык общения с клиентом (en или ru)
    Culture = forms.CharField(max_length=10, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        self.fields['SignatureValue'].initial = self.calc_signature()

    def get_redirect_url(self):
        """
            Получить URL с GET-параметрами, соответствующими значениям полей в
            форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
            ручной отправке формы методом GET.
        """
        params = {}
        for fieldname, field in self.fields.items():
            value = self.initial.get(fieldname, field.initial)
            if value:
                params[fieldname] = value

        return '{}?{}'.format(self.target, urlencode(params))


class ResultURLForm(BaseRobokassaForm):
    """
        Форма для обработки результата оплаты
    """
    SIGNATURE_FIELDS = ('OutSum', 'InvId')
    PASSWD = conf.PASSWORD2

    OutSum = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    InvId = forms.IntegerField(min_value=0)
    SignatureValue = forms.CharField(max_length=32)

    def clean(self):
        try:
            signature = self.cleaned_data['SignatureValue'].upper()
        except KeyError:
            raise forms.ValidationError(_('Undefined signature'))

        if signature != self.calc_signature():
            raise forms.ValidationError(_('Invalid signature'))

        return self.cleaned_data
