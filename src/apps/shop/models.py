from uuid import uuid4
from django.db import models
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.timezone import now
from django.core.validators import MinValueValidator, RegexValidator
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
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('shop:index')


class CategoryQuerySet(AliasedQuerySetMixin, models.QuerySet):
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


class CategoryTreeManager(TreeManager):
    _queryset_class = CategoryQuerySet


class Category(MPTTModel):
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
    is_visible = models.BooleanField(_('visible'), default=False)
    sort_order = models.PositiveIntegerField(_('sort order'))

    objects = CategoryTreeManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        order_insertion_by = ('sort_order', )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Category.objects.rebuild()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('shop:category', category_alias=self.alias)


class ProductQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        visible = kwargs.pop('visible', None)
        if visible is None:
            pass
        elif visible:
            qs &= models.Q(is_visible=True)
        else:
            qs &= models.Q(is_visible=False)
        return qs


class Product(models.Model):
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
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), related_name='products')
    photo = StdImageField(_('photo'),
        storage=MediaStorage('shop/product'),
        min_dimensions=(180, 60),
        admin_variation='admin',
        crop_area=True,
        variations=dict(
            normal=dict(
                size=(300, 300),
                crop=False,
            ),
            small=dict(
                size=(120, 120),
                crop=False,
            ),
            admin=dict(
                size=(200, 200),
                crop=False,
            ),
        ),
    )
    description = CKEditorField(_('description'),
        editor_options=settings.CKEDITOR_CONFIG_MEDIUM,
        blank=True
    )
    price = ValuteField(_('price'), validators=[MinValueValidator(0)])
    is_visible = models.BooleanField(_('visible'), default=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)
    sort_order = models.PositiveIntegerField(_('sort order'))

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('is_visible', 'sort_order',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('shop:detail', category_alias=self.main_category.alias, alias=self.alias)

    @property
    def main_category(self):
        return self.categories.first()


class OrderQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        payed = kwargs.pop('payed', None)
        if payed is None:
            pass
        elif payed:
            qs &= models.Q(status=Order.STATUS_PAID)
        else:
            qs &= models.Q(status=Order.STATUS_NOT_PAID)
        return qs


class Order(models.Model):
    """ Заказ """
    STATUS_NOT_PAID = 1
    STATUS_PAID = 2
    STATUS = (
        (STATUS_NOT_PAID, _('Not paid')),
        (STATUS_PAID, _('Paid')),
    )

    status = models.PositiveSmallIntegerField(_('status'), default=STATUS_NOT_PAID, choices=STATUS)

    pay_date = models.DateTimeField(_('pay date'), null=True, editable=False)
    products_cost = ValuteField(_('products cost'),
        validators=[MinValueValidator(0)],
        editable=False
    )
    hash = models.CharField(_('hash'),
        max_length=32,
        unique=True,
        validators=[RegexValidator('^[0-9a-f]{32}$')],
        editable=False,
    )
    session = models.CharField(_('session'), max_length=64, editable=False)
    date = models.DateTimeField(_('create date'), editable=False)

    objects = OrderQuerySet.as_manager()

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

    def make_hash(self):
        if not self.hash:
            self.hash = str(uuid4()).replace('-', '')
        return self.hash

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
    order = models.ForeignKey(Order, verbose_name=_('order'), related_name='order_products')
    product = models.ForeignKey(Product, verbose_name=_('product'))
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
