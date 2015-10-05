from django.db import transaction
from django.dispatch import receiver
from django.db.models import QuerySet, F
from django.db.models.expressions import RawSQL
from django.db.models.signals import post_delete
from django.db.models.query import ValuesListQuerySet
from ..models import ShopCategory, ShopProduct
from . import products_changed, categories_changed


@receiver(products_changed, sender=ShopProduct)
def recalculate_product_count(sender, **kwargs):
    """
        Обработчик события изменения кол-ва видимых продуктов,
        привязанных непосредственно к категории
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
def recalculate_total_product_count(sender, **kwargs):
    """
        Обработчик события изменения кол-ва видимых продуктов,
        привязанных к категории и её подкатегориям
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
def delete_product(sender, **kwargs):
    """
        Удаление продукта.
        Если продукт был видимый - вызываем сигнал изменения кол-ва видимых продуктов
    """
    instance = kwargs.get('instance')
    if isinstance(instance, ShopProduct) and instance.is_visible:
        products_changed.send(sender, categories=instance.category_id)