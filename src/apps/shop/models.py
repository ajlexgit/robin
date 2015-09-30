from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.db.models.expressions import RawSQL
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from ckeditor.fields import CKEditorField
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.stdimage.fields import StdImageField
from libs.media_storage import MediaStorage
from libs.valute_field import ValuteField
from libs.autoslug import AutoSlugField
from libs.mptt import *


class ShopConfig(SingletonModel):
    title = models.CharField(_('title'), max_length=128)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('shop:index')


class ShopCategoryQuerySet(AliasedQuerySetMixin, MPTTQuerySet):
    def aliases(self, qs, kwargs):
        visible = kwargs.pop('visible', None)
        if visible is None:
            pass
        elif visible:
            qs &= models.Q(is_visible=True)
        else:
            qs &= models.Q(is_visible=False)
        return qs


class ShopCategoryTreeManager(MPTTQuerySetManager):
    _queryset_class = ShopCategoryQuerySet

    def reset_product_count(self, leaf_queryset=None):
        """
            Устанавливает корректное значение products_count всем категориям.
            Значение immediate_products_count должно быть уже установлено и корректно.
        """
        if leaf_queryset is None:
            tree_row = self.get_leafnodes()
        else:
            tree_row = leaf_queryset

        tree_row.update(
            product_count=RawSQL(
                '(SELECT COUNT(*) '
                'FROM shop_shopproduct AS ssp '
                'WHERE ssp.category_id = shop_shopcategory.id '
                'AND ssp.is_visible = TRUE)',
                ()
            )
        )

        while True:
            parent_ids = tuple(tree_row.exclude(
                parent=None
            ).distinct().order_by('parent_id').values_list(
                'parent_id',
                flat=True
            ))
            if not parent_ids:
                break

            tree_row = self.filter(pk__in=parent_ids)
            tree_row.update(
                product_count=RawSQL(
                    '(SELECT COUNT(*) '
                    'FROM shop_shopproduct AS ssp '
                    'WHERE ssp.category_id = shop_shopcategory.id '
                    'AND ssp.is_visible = TRUE)'
                    ' + '
                    '(SELECT COALESCE(SUM(ssc.product_count), 0) '
                    'FROM shop_shopcategory AS ssc '
                    'WHERE ssc.parent_id = shop_shopcategory.id)', ()
                )
            )


class ShopCategory(MPTTModel):
    """ Категория товаров """
    parent = TreeForeignKey('self',
        blank=True,
        null=True,
        verbose_name=_('parent category'),
        related_name='children'
    )
    title = models.CharField(_('title'), max_length=128)
    alias = AutoSlugField(_('alias'),
        populate_from=('title',),
        unique=True,
        help_text=_('Leave it blank to auto generate it')
    )
    is_visible = models.BooleanField(_('visible'), default=False, db_index=True)
    product_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text=_('count of visible products'),
    )
    sort_order = models.PositiveIntegerField(_('sort order'))

    objects = ShopCategoryTreeManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        order_insertion_by = ('sort_order', )

    def save(self, *args, **kwargs):
        is_add = self.pk is None
        original = None if is_add else self.__class__.objects.select_related('parent').only(
            'is_visible', 'parent'
        ).get(pk=self.pk)

        if self.is_visible and self.parent_id and not self.parent.is_visible:
            # корректировка для случая видимой подкатегории в невидимой
            if is_add:
                # если добавление - скрываем текущую категорию
                self.is_visible = False
            elif self.parent.id != original.parent_id:
                # если смена родителя - скрываем текущую категорию и её потомков
                self.is_visible = False
                self.get_descendants().filter(is_visible=True).update(is_visible=False)
            else:
                # если смена видимости - показываем предков
                self.get_ancestors().filter(is_visible=False).update(is_visible=True)
        elif not is_add and not self.is_visible:
            # скрытие категории - скрываем потомков
            self.get_descendants().filter(is_visible=True).update(is_visible=False)

        super().save(*args, **kwargs)
        # self.__class__.objects.rebuild()

    def __str__(self):
        return self.title

    @cached_property
    def descendant_products(self):
        """ Продукты категории и её подкатегорий """
        return ShopProduct.objects.filter(
            visible=True,
            category__in=self.get_descendants(include_self=True).filter(visible=True)
        ).distinct()

    @staticmethod
    def autocomplete_item(obj):
        return {
            'id': obj.pk,
            'text': '–' * obj.level + obj.title,
        }

    def get_absolute_url(self):
        return resolve_url('shop:category', category_alias=self.alias)


class ShopProductQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        visible = kwargs.pop('visible', None)
        if visible is None:
            pass
        elif visible:
            qs &= models.Q(is_visible=True)
        else:
            qs &= models.Q(is_visible=False)
        return qs


class ShopProduct(models.Model):
    """ Товар """
    title = models.CharField(_('title'), max_length=128)
    alias = AutoSlugField(_('alias'),
        populate_from=('title',),
        unique=True,
        help_text=_('Leave it blank to auto generate it')
    )
    serial = models.SlugField(_('S/N'),
        max_length=64,
        unique=True,
        help_text=_('Unique identifier of the product')
    )
    category = models.ForeignKey(ShopCategory,
        verbose_name=_('category'),
        related_name='products'
    )
    photo = StdImageField(_('photo'),
        storage=MediaStorage('shop/product'),
        min_dimensions=(180, 60),
        admin_variation='admin',
        crop_area=True,
        crop_field='photo_crop',
        variations=dict(
            normal=dict(
                size=(300, 300),
                crop=False,
            ),
            small=dict(
                size=(160, 160),
                crop=False,
            ),
            admin=dict(
                size=(200, 200),
                crop=False,
            ),
            admin_micro=dict(
                size=(60, 60),
                crop=False,
                background=(255,255,255,255),
            )
        ),
    )
    photo_crop = models.CharField(_('stored_crop'),
        max_length=32,
        blank=True,
        editable=False,
    )
    description = CKEditorField(_('description'),
        editor_options=settings.CKEDITOR_CONFIG_MEDIUM,
        blank=True
    )
    price = ValuteField(_('price'), validators=[MinValueValidator(0)])
    is_visible = models.BooleanField(_('visible'), default=False)
    created = models.DateTimeField(_('create date'), default=now, editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    objects = ShopProductQuerySet.as_manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        index_together = (('category', 'is_visible'),)
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('shop:detail',
            category_alias=self.category.alias,
            alias=self.alias
        )

    def save(self, *args, **kwargs):
        is_add = self.pk is None
        original = None if is_add else self.__class__.objects.select_related('category').only(
            'is_visible', 'category'
        ).get(pk=self.pk)

        if is_add:
            # добавлен видимый продукт
            if self.is_visible:
                self.category.get_ancestors(include_self=True).update(
                    immediate_product_count=models.F('immediate_product_count') + 1,
                    product_count=models.F('product_count') + 1,
                )
        elif self.category != original.category:
            # сменили категорию продукта
            if original.is_visible:
                original.category.get_ancestors(include_self=True).update(
                    immediate_product_count=models.F('immediate_product_count') - 1,
                    product_count=models.F('product_count') - 1,
                )
            if self.is_visible:
                self.category.get_ancestors(include_self=True).update(
                    immediate_product_count=models.F('immediate_product_count') + 1,
                    product_count=models.F('product_count') + 1,
                )
        elif self.is_visible and not original.is_visible:
            # продукт стал видимым
            self.category.get_ancestors(include_self=True).update(
                immediate_product_count=models.F('immediate_product_count') + 1,
                product_count=models.F('product_count') + 1,
            )
        elif not self.is_visible and original.is_visible:
            # продукт стал скрытым
            self.category.get_ancestors(include_self=True).update(
                immediate_product_count=models.F('immediate_product_count') - 1,
                product_count=models.F('product_count') - 1,
            )

        super().save(*args, **kwargs)


class ShopOrderQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        payed = kwargs.pop('payed', None)
        if payed is None:
            pass
        elif payed:
            qs &= models.Q(status=ShopOrder.STATUS_PAID)
        else:
            qs &= models.Q(status=ShopOrder.STATUS_NOT_PAID)
        return qs


class ShopOrder(models.Model):
    """ Заказ """
    STATUS_NOT_PAID = 1
    STATUS_PAID = 2
    STATUS = (
        (STATUS_NOT_PAID, _('Not paid')),
        (STATUS_PAID, _('Paid')),
    )

    status = models.PositiveSmallIntegerField(_('status'),
        default=STATUS_NOT_PAID,
        choices=STATUS,
    )
    pay_date = models.DateTimeField(_('pay date'),
        null=True,
        editable=False,
    )
    products_cost = ValuteField(_('products cost'),
        validators=[MinValueValidator(0)],
        editable=False,
    )
    session = models.CharField(_('session'), max_length=64, editable=False)
    date = models.DateTimeField(_('create date'), editable=False)

    objects = ShopOrderQuerySet.as_manager()

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-date', )

    def __str__(self):
        return 'Order #%s' % self.pk

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = now()

        self.make_hash()
        super().save(*args, **kwargs)

    @property
    def total_cost(self):
        return self.products_cost

    def mark_payed(self, save=False):
        if self.status == self.STATUS_NOT_PAID:
            self.status = self.STATUS_PAID
            self.pay_date = now()
            if save:
                self.save()


class OrderProduct(models.Model):
    """ Продукты заказа """
    order = models.ForeignKey(ShopOrder, verbose_name=_('order'), related_name='order_products')
    product = models.ForeignKey(ShopProduct, verbose_name=_('product'))
    order_price = ValuteField(_('price per item'), validators=[MinValueValidator(0)])
    count = models.PositiveSmallIntegerField(_('count'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        unique_together = ('order', 'product')

    @property
    def total_cost(self):
        return self.order_price * self.count

    def __str__(self):
        return '%s (x%s)' % (self.product.title, self.count)
