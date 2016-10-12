from decimal import Decimal, InvalidOperation
from django.utils.translation import ugettext_lazy as _
from libs.valute_field import Valute


class BaseStrategy:
    name = ''
    description = ''

    @classmethod
    def short_description(cls, promo):
        raise NotImplementedError

    @classmethod
    def full_description(cls, promo):
        raise NotImplementedError

    @classmethod
    def validate(cls, form, cleaned_data):
        return cleaned_data

    @classmethod
    def calculate(cls, promo, order):
        raise NotImplementedError


class FixedAmountStrategy(BaseStrategy):
    """ Фиксированная скидка, например 100 рублей """
    name = 'fixed_amount'
    description = _('Fixed amount')

    @classmethod
    def short_description(cls, promo):
        return '-%s' % Valute(promo.parameter)

    @classmethod
    def full_description(cls, promo):
        return _('Discount %s') % Valute(promo.parameter)

    @classmethod
    def validate(cls, form, cleaned_data):
        parameter = cleaned_data.get('parameter', '')
        if not parameter:
            form.add_error('parameter', _('This field cannot be blank.'))
            return

        try:
            amount = Valute(parameter)
        except (TypeError, ValueError, InvalidOperation):
            form.add_error('parameter', _('Invalid value'))
            return

        if not amount:
            form.add_error('parameter', _('Ensure this value is greater than 0'))
            return

        return cleaned_data

    @classmethod
    def calculate(cls, promo, order):
        amount = Valute(promo.parameter)
        return amount


class PercentageStrategy(BaseStrategy):
    """ Процентная скидка, например 10% """
    name = 'percent'
    description = _('By a percent')

    @classmethod
    def short_description(cls, promo):
        return '-%s%%' % Decimal(promo.parameter)

    @classmethod
    def full_description(cls, promo):
        return _('Discount %s%%') % Decimal(promo.parameter)

    @classmethod
    def validate(cls, form, cleaned_data):
        parameter = cleaned_data.get('parameter', '')
        if not parameter:
            form.add_error('parameter', _('This field cannot be blank.'))
            return

        try:
            percentage = Decimal(parameter)
        except (TypeError, ValueError, InvalidOperation):
            form.add_error('parameter', _('Invalid value'))
            return

        if not percentage:
            form.add_error('parameter', _('Ensure this value is greater than 0'))
            return

        return cleaned_data

    @classmethod
    def calculate(cls, promo, order):
        percentage = Decimal(promo.parameter)
        return order.products_cost * percentage / 100


ALL_STRATEGIES = (FixedAmountStrategy, PercentageStrategy)
STRATEGIES = {
    strategy.name: strategy
    for strategy in ALL_STRATEGIES
}
STRATEGY_CHOICES = tuple(
    (strategy.name, strategy.description)
    for strategy in ALL_STRATEGIES
)
