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
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from libs.aliased_queryset import AliasedQuerySetMixin
from libs.stdimage.fields import StdImageField
from libs.media_storage import MediaStorage
from libs.valute_field import ValuteField
from libs.autoslug import AutoSlugField


class ShopConfig(SingletonModel):
    title = models.CharField(_('title'), max_length=128)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('shop:index')


class ShopCategoryQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        visible = kwargs.pop('visible', None)
        if visible is None:
            pass
        elif visible:
            qs &= models.Q(is_visible=True)
        else:
            qs &= models.Q(is_visible=False)
        return qs

    def only(self, *fields):
        """ Fix for MPTT """
        mptt_meta = self.model._mptt_meta
        mptt_fields = tuple(
            getattr(mptt_meta, key)
            for key in ('left_attr', 'right_attr', 'tree_id_attr', 'level_attr')
        )
        final_fields = set(mptt_fields + fields + tuple(mptt_meta.order_insertion_by))
        return super().only(*final_fields)

    def reset_immediate_products_count(self):
        """
            Установка корректного значения immediate_products_count
        """
        self.update(
            immediate_product_count=RawSQL(
                'SELECT COUNT(*) '
                'FROM shop_shopproduct '
                'WHERE shop_shopproduct.category_id = shop_shopcategory.id '
                'AND shop_shopproduct.is_visible=TRUE', ()
            )
        )


class ShopCategoryTreeManager(TreeManager):
    _queryset_class = ShopCategoryQuerySet


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
    immediate_product_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text=_('count of immediate visible products'),
    )
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
        original = None if is_add else self.__class__.objects.select_related('parent').get(pk=self.pk)

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
