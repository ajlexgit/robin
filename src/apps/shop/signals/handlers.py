from django.dispatch import receiver
from django.db.models import QuerySet
from django.db.models.expressions import RawSQL
from django.db.models.signals import post_delete
from django.db.models.query import ValuesListQuerySet
from ..models import ShopCategory, ShopProduct
from . import visible_products_changed


@receiver(visible_products_changed, sender=ShopProduct)
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
        raise TypeError('Invalid categories for signal "visible_products_changed"')

    categories.update(
        product_count=RawSQL(
            '(SELECT COUNT(*) '
            'FROM shop_shopproduct AS ssp '
            'WHERE ssp.category_id = shop_shopcategory.id '
            'AND ssp.is_visible = TRUE)',
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
        visible_products_changed.send(sender, categories=instance.category_id)