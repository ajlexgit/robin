from django.db import transaction
from django.dispatch import receiver
from django.db.models import QuerySet, F
from django.db.models.expressions import RawSQL
from django.db.models.signals import post_delete
from django.db.models.query import ValuesListQuerySet
from django.utils.translation import ugettext_lazy as _
from libs.email import send
from ..models import ShopCategory, ShopProduct, ShopOrder, NotifyReceiver
from . import products_changed, categories_changed, order_confirmed, order_cancelled, order_paid


@receiver(products_changed, sender=ShopProduct)
def products_changed_handler(sender, **kwargs):
    """
        Обработчик события изменения кол-ва видимых продуктов,
        привязанных непосредственно к категории.

        Используется для обновления счетчиков товаров в каждой категории.
    """
    categories = kwargs.get('categories')
    if isinstance(categories, ShopCategory):
        # экземпляр категории
        categories = ShopCategory.objects.filter(pk=categories.pk)
    elif isinstance(categories, (int, str)):
        # строка или число, являющееся ID категории
        categories = ShopCategory.objects.filter(pk=categories)
    elif isinstance(categories, (list, tuple, ValuesListQuerySet)):
        # список строк или чисел, являющихся ID категории
        categories = ShopCategory.objects.filter(pk__in=categories)
    elif isinstance(categories, QuerySet) and categories.model == ShopCategory:
        # QuerySet категорий
        pass
    else:
        raise TypeError('Invalid categories for signal "products_changed"')

    with transaction.atomic():
        categories.update(
            product_count=RawSQL(
                '(SELECT COUNT(*) '
                'FROM shop_shopproduct AS ssp '
                'WHERE ssp.category_id = shop_shopcategory.id '
                'AND ssp.is_visible = TRUE)',
                ()
            )
        )
        categories.update(
            total_product_count=F('product_count')
        )

    categories_changed.send(ShopCategory, categories=categories)


@receiver(categories_changed, sender=ShopCategory)
def categories_changed_handler(sender, **kwargs):
    """
        Обработчик события изменения кол-ва видимых продуктов,
        привязанных к категории и её подкатегориям.

        Используется для обновления счетчиков товаров в каждой категории.
    """
    categories = kwargs.get('categories')
    include_self = kwargs.get('include_self', True)
    if isinstance(categories, ShopCategory):
        # экземпляр категории
        categories = ShopCategory.objects.filter(pk=categories.pk)
    elif isinstance(categories, (int, str)):
        # строка или число, являющееся ID категории
        categories = ShopCategory.objects.filter(pk=categories)
    elif isinstance(categories, (list, tuple, ValuesListQuerySet)):
        # список строк или чисел, являющихся ID категории
        categories = ShopCategory.objects.filter(pk__in=categories)
    elif isinstance(categories, QuerySet) and categories.model == ShopCategory:
        # QuerySet категорий
        pass
    else:
        raise TypeError('Invalid categories for signal "categories_changed"')

    ancestors = categories.get_ancestors(
        include_self=include_self
    ).filter(
        is_visible=True
    ).order_by('tree_id', '-level').values_list('id', flat=True)

    with transaction.atomic():
        for category_id in ancestors:
            ShopCategory.objects.filter(pk=category_id).update(
                total_product_count=RawSQL(
                    'SELECT shop_shopcategory.product_count + '
                    'COALESCE(SUM(ssc.total_product_count), 0) '
                    'FROM shop_shopcategory AS ssc '
                    'WHERE ssc.parent_id = shop_shopcategory.id '
                    'AND ssc.is_visible = TRUE',
                    ()
                )
            )


@receiver(post_delete, sender=ShopProduct)
def post_delete_handler(sender, **kwargs):
    """
        Обработчик события удаления продукта.
        Если продукт был видимый - вызываем сигнал изменения кол-ва видимых продуктов.
    """
    instance = kwargs.get('instance')
    if isinstance(instance, ShopProduct) and instance.is_visible:
        products_changed.send(sender, categories=instance.category_id)


@receiver(order_confirmed, sender=ShopOrder)
def order_confirmed_handler(sender, **kwargs):
    """
        Обработчик сигнала подтверждения заказа пользователем.
    """
    order = kwargs.get('order')
    if not order or not isinstance(order, ShopOrder):
        return

    # TODO: paste your code here


@receiver(order_paid, sender=ShopOrder)
def order_paid_handler(sender, **kwargs):
    """
        Обработчик сигнала оплаты заказа
    """
    order = kwargs.get('order')
    if not order or not isinstance(order, ShopOrder):
        return

    # TODO: paste your code here

    request = kwargs.get('request')

    receivers = NotifyReceiver.objects.all().values_list('email', flat=True)
    if receivers:
        send(request, receivers,
            subject=_('New order at {domain}'),
            template='shop/mails/new_order.html',
            context={
                'order': order,
            }
        )


@receiver(order_cancelled, sender=ShopOrder)
def order_cancelled_handler(sender, **kwargs):
    """
        Обработчик сигнала отмены заказа пользователем.
    """
    order = kwargs.get('order')
    if not order or not isinstance(order, ShopOrder):
        return

    # TODO: paste your code here
