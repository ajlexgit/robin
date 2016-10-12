from django.contrib.contenttypes.models import ContentType
from .models import PromoCode


def get_promocodes(order):
    """
        Получение промокодов, привязанных к заказу.
    """
    ct = ContentType.objects.get_for_model(order.__class__)
    promocodes = tuple(PromoCode.objects.filter(
        usages__content_type=ct,
        usages__object_id=order.pk,
    ).distinct())

    for promocode in promocodes:
        promocode.calculated_discount = promocode.calculate(order)

    return promocodes
