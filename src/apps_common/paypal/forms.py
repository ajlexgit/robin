from urllib.parse import urlencode
from django import forms
from django.shortcuts import resolve_url
from . import conf

FIELD_NAME_MAPPING = {
    'description': 'item_name',

    'result_url': 'notify_url',
    'success_url': 'return',
    'cancel_url': 'cancel_return',
}


class BasePayPalForm(forms.Form):
    """
        Базовая форма PayPal
    """

    # Параметр с URL'ом, на который будет отправлена форма.
    # Может пригодиться для использования в шаблоне.
    target = conf.FORM_TARGET

    # Тип действия (значение)
    COMMAND = ''

    # Обязательные поля. Не имеет отношения к валидации формы.
    # Перечисляются поля, в которых должно быть заполнено
    # начальное значение при создании формы
    REQUIRE_INITIAL = ()

    # аккаунт магазина
    business = forms.CharField(max_length=255, initial=conf.EMAIL)

    # Тип действия (поле формы)
    cmd = forms.CharField(max_length=32)

    # кодировка
    charset = forms.CharField(max_length=32, initial='utf-8', required=False)

    # не требовать адрес
    no_shipping = forms.CharField(max_length=1, initial='1', required=False)

    # не предлагать вводить примечание
    no_note = forms.CharField(max_length=1, initial='1', required=False)

    # адрес, обрабатывающий уведомления о платежах
    result_url = forms.URLField(max_length=255)

    # адреса для редиректа пользователей
    success_url = forms.URLField(max_length=1024)
    cancel_url = forms.URLField(max_length=1024)

    # Метод перехода на success_url
    rm = forms.CharField(max_length=1, initial='0')

    # Дополнительное поле для нужд разработчика
    custom = forms.CharField(max_length=256, required=False)

    def __init__(self, request, *args, **kwargs):
        kwargs.setdefault('auto_id', '')
        super().__init__(*args, **kwargs)
        self.initial['cmd'] = self.COMMAND
        self._initial_url(request, 'result_url', conf.RESULT_URL)
        self._initial_url(request, 'success_url', conf.SUCCESS_URL)
        self._initial_url(request, 'cancel_url', conf.CANCEL_URL)

        # скрытый виджет по умолчанию для всех полей
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        for fieldname in self.REQUIRE_INITIAL:
            value = self.initial.get(fieldname)
            if not value:
                raise ValueError('"%s" field requires initial value' % fieldname)

    def add_prefix(self, field_name):
        """ Замена имен полей """
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

    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)

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


class PaymentForm(BasePayPalForm):
    """
        Форма для разового платежа
    """
    COMMAND = '_xclick'
    REQUIRE_INITIAL = ('invoice', 'amount', 'description', )

    # ID заказа
    invoice = forms.CharField(max_length=127)

    # ID товара
    item_number = forms.CharField(max_length=127, required=False)

    # цена товара
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # описание покупки
    description = forms.CharField(max_length=127)

    # Количество единиц товара
    quantity = forms.IntegerField(min_value=0, initial='1', required=False)

    # валюта оплаты
    currency_code = forms.CharField(max_length=3, initial=conf.CURRENCY)


class AddToCartForm(BasePayPalForm):
    """
        Форма для добавления товара в корзину PayPal
    """
    COMMAND = '_cart'
    REQUIRE_INITIAL = ('amount', 'description', )

    # Подвид действия - добавление товара
    add = forms.CharField(max_length=1, initial='1')

    # ID заказа
    invoice = forms.CharField(max_length=127)

    # ID товара
    item_number = forms.CharField(max_length=127, required=False)

    # цена товара
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # описание покупки
    description = forms.CharField(max_length=127)

    # Количество единиц товара
    quantity = forms.IntegerField(min_value=0, initial='1', required=False)

    # валюта оплаты
    currency_code = forms.CharField(max_length=3, initial=conf.CURRENCY)

    # Ссылка, куда переходит юзер, чтобы продолжить покупки
    shopping_url = forms.URLField(max_length=255, required=False)


class DisplayCartForm(BasePayPalForm):
    """
        Форма для просмотра корзины PayPal
    """
    COMMAND = '_cart'
    REQUIRE_INITIAL = ()

    # Подвид действия - просмотр корзины
    display = forms.CharField(max_length=1, initial='1')

    # Ссылка, куда переходит юзер, чтобы продолжить покупки
    shopping_url = forms.URLField(max_length=255, required=False)


class DonationForm(BasePayPalForm):
    """
        Форма для пожертвований
    """
    COMMAND = '_donations'
    REQUIRE_INITIAL = ()

    # ID заказа
    invoice = forms.CharField(max_length=127)

    # цена товара
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # описание покупки
    description = forms.CharField(max_length=127)

    # валюта оплаты
    currency_code = forms.CharField(max_length=3, initial=conf.CURRENCY)


class PayPalResultForm(forms.Form):
    """
        Форма для обработки результата оплаты
    """
    payment_status = forms.CharField(max_length=32)
    receiver_email = forms.EmailField()
    invoice = forms.CharField(max_length=127, required=False)
    mc_gross = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
