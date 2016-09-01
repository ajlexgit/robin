import uuid
from django.db import models
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from gallery import *
from solo.models import SingletonModel
from ckeditor.fields import CKEditorField
from libs.mptt import *
from libs.autoslug import AutoSlugField
from libs.valute_field import ValuteField
from libs.aliased_queryset import AliasedQuerySetMixin
from .signals import products_changed, categories_changed


class ShopConfig(SingletonModel):
    """ Главная страница """
    header = models.CharField(_('header'), max_length=128)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('shop:index')

    def __str__(self):
        return self.header


class ShopCategoryQuerySet(AliasedQuerySetMixin, MPTTQuerySet):
    def aliases(self, qs, kwargs):
        visible = kwargs.pop('visible', None)
        if visible is None:
            pass
        elif visible:
            qs &= models.Q(is_visible=True, total_product_count__gt=0)
        else:
            qs &= ~models.Q(is_visible=True, total_product_count__gt=0)
        return qs


class ShopCategoryTreeManager(MPTTQuerySetManager):
    _queryset_class = ShopCategoryQuerySet

    def root_categories(self):
        return self.root_nodes().filter(visible=True)


class ShopCategory(MPTTModel):
    """ Категория товаров """
    parent = TreeForeignKey('self',
        blank=True,
        null=True,
        verbose_name=_('parent category'),
        related_name='children'
    )
    title = models.CharField(_('title'), max_length=128)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    product_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text=_('count of immediate visible products'),
    )
    total_product_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text=_('count of visible products'),
    )
    is_visible = models.BooleanField(_('visible'), default=True, db_index=True)
    created = models.DateTimeField(_('create date'), default=now, editable=False)
    updated = models.DateTimeField(_('change date'), auto_now=True)
    sort_order = models.IntegerField(_('order'), default=0)

    objects = ShopCategoryTreeManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        order_insertion_by = ('sort_order', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('shop:category', category_slug=self.slug)

    def save(self, *args, **kwargs):
        is_add = self.pk is None
        original = None if is_add else self.__class__.objects.select_related('parent').only(
            'is_visible', 'parent'
        ).get(pk=self.pk)

        # Видимость
        if self.is_visible and self.parent_id and not self.parent.is_visible:
            # корректировка для случая видимой подкатегории в невидимой
            if is_add:
                # если добавление - скрываем текущую категорию
                self.is_visible = False
            elif self.parent_id != original.parent_id:
                # если смена родителя - скрываем текущую категорию и её потомков
                self.is_visible = False
                self.get_descendants().filter(is_visible=True).update(is_visible=False)
            else:
                # если смена видимости - показываем предков
                self.get_ancestors().filter(is_visible=False).update(is_visible=True)
        elif not is_add and not self.is_visible and original.is_visible:
            # скрытие категории - скрываем потомков
            self.get_descendants().filter(is_visible=True).update(is_visible=False)

        super().save(*args, **kwargs)

        # Кол-во продуктов
        if is_add:
            pass
        elif self.parent_id != original.parent_id:
            # смена родителя
            categories = []
            if self.parent_id:
                categories.append(self.parent_id)
            if original.parent_id:
                categories.append(original.parent_id)
            if categories:
                categories_changed.send(self.__class__, categories=categories)
        elif self.is_visible and not original.is_visible:
            # категория показана
            categories_changed.send(self.__class__, categories=self.pk)
        elif not self.is_visible and original.is_visible:
            # категория скрыта
            self.get_descendants(include_self=True).update(total_product_count=0)
            categories_changed.send(self.__class__, categories=self.pk, include_self=False)

    @cached_property
    def subcategories(self):
        """ Видимые дочерние подкатегории """
        return self.get_children().filter(visible=True)

    @cached_property
    def products(self):
        """ Видимые продукты категории и её подкатегорий """
        return ShopProduct.objects.filter(
            visible=True,
            category__in=self.get_descendants(include_self=True).filter(visible=True)
        ).distinct()

    @staticmethod
    def autocomplete_item(obj):
        return {
            'id': obj.pk,
            'text': '–' * obj.level + ' ' + obj.title,
        }


class ShopProductQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        visible = kwargs.pop('visible', None)
        if visible is None:
            pass
        elif visible:
            qs &= models.Q(is_visible=True)
        else:
            qs &= models.Q(is_visible=False)

        supercategory = kwargs.pop('supercategory', None)
        if supercategory is None:
            pass
        else:
            if isinstance(supercategory, (str, int)):
                supercategory = ShopCategory.objects.get(pk=supercategory)

            categories = supercategory.get_descendants(include_self=True).filter(visible=True)
            qs &= models.Q(category__in=categories)

        return qs


class ShopProductGalleryImageItem(GalleryImageItem):
    """ Элемент галереи продукта """
    STORAGE_LOCATION = 'shop/product/gallery'
    MIN_DIMENSIONS = (100, 60)
    ADMIN_CLIENT_RESIZE = True

    SHOW_VARIATION = 'normal'
    ASPECTS = 'normal'
    ADMIN_VARIATION = 'admin'
    VARIATIONS = dict(
        normal=dict(
            size=(300, 300),
            crop=False,
        ),
        admin=dict(
            size=(160, 120),
            crop=False,
            background=(255, 255, 255, 255),
        ),
        admin_micro=dict(
            size=(40, 40),
            crop=False,
            background=(255, 255, 255, 255),
        )
    )


class ShopProductGallery(GalleryBase):
    """ Галерея продукта """
    IMAGE_MODEL = ShopProductGalleryImageItem


class ShopProduct(models.Model):
    """ Продукт """
    category = models.ForeignKey(ShopCategory,
        verbose_name=_('category'),
        related_name='immediate_products'
    )
    title = models.CharField(_('title'), max_length=128)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    gallery = GalleryField(ShopProductGallery, verbose_name=_('gallery'), blank=True, null=True)
    description = CKEditorField(_('description'), blank=True)
    price = ValuteField(_('price'))
    is_visible = models.BooleanField(_('visible'), default=True)
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
            category_slug=self.category.slug,
            slug=self.slug
        )

    def save(self, *args, **kwargs):
        is_add = self.pk is None
        if is_add:
            original = None
        else:
            original = self.__class__.objects.only(
                'is_visible', 'category_id'
            ).get(pk=self.pk)

        super().save(*args, **kwargs)

        if is_add:
            # добавление видимого продукта
            if self.is_visible:
                products_changed.send(
                    self.__class__,
                    categories=self.category_id
                )
        elif self.category_id != original.category_id:
            # смена категории
            categories = []
            if original.is_visible:
                categories.append(original.category_id)
            if self.is_visible:
                categories.append(self.category_id)

            if categories:
                products_changed.send(
                    self.__class__,
                    categories=categories
                )
        elif self.is_visible != original.is_visible:
            # смена видимости
            products_changed.send(
                self.__class__,
                categories=self.category_id
            )

    @cached_property
    def photo(self):
        if self.gallery:
            item = self.gallery.image_items.first()
            return item.image if item else None
        return None


class ShopOrderQuerySet(AliasedQuerySetMixin, models.QuerySet):
    def aliases(self, qs, kwargs):
        # подтвержденные
        confirmed = kwargs.pop('confirmed', None)
        if confirmed is None:
            pass
        else:
            qs &= models.Q(is_confirmed=confirmed)

        # отмененные
        cancelled = kwargs.pop('cancelled', None)
        if cancelled is None:
            pass
        else:
            qs &= models.Q(is_cancelled=cancelled)

        # оплаченные
        paid = kwargs.pop('paid', None)
        if paid is None:
            pass
        else:
            qs &= models.Q(is_paid=paid)

        # проверенные
        checked = kwargs.pop('checked', None)
        if checked is None:
            pass
        else:
            qs &= models.Q(is_checked=checked)

        # в архиве
        archived = kwargs.pop('archived', None)
        if archived is None:
            pass
        else:
            qs &= models.Q(is_archived=archived)

        return qs


class ShopOrder(models.Model):
    """ Заказ """
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, unique=True, editable=False)
    session = models.CharField(_('session'), max_length=64, editable=False)

    # Подтвержден плательщиком
    is_confirmed = models.BooleanField(_('confirmed'), default=False, editable=False)
    confirm_date = models.DateTimeField(_('confirm date'),
        null=True,
        editable=False,
    )

    # Отменен плательщиком
    is_cancelled = models.BooleanField(_('cancelled'), default=False)
    cancel_date = models.DateTimeField(_('cancel date'),
        null=True,
        editable=False,
    )

    # Проверка менеджером
    is_checked = models.BooleanField(_('checked'), default=False)
    check_date = models.DateTimeField(_('check date'),
        null=True,
        editable=False,
    )

    # Оплачен
    is_paid = models.BooleanField(_('paid'), default=False)
    pay_date = models.DateTimeField(_('pay date'),
        null=True,
        editable=False,
    )

    # В архиве
    is_archived = models.BooleanField(_('archived'), default=False)
    archivation_date = models.DateTimeField(_('archivation date'),
        null=True,
        editable=False,
    )

    products_cost = ValuteField(_('products cost'), editable=False)
    created = models.DateTimeField(_('create date'), default=now, editable=False)

    objects = ShopOrderQuerySet.as_manager()

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-created', )

    def __str__(self):
        return _('Order #%s') % self.pk

    def clean(self):
        errors = {}

        # неподтвержденный заказ не может быть проверен или оплачен
        if not self.is_confirmed:
            if self.is_checked:
                errors['is_checked'] = _('Unconfirmed order can\'t be checked')
            if self.is_paid:
                errors['is_paid'] = _('Unconfirmed order can\'t be paid')

        if errors:
            raise ValidationError(errors)

    def calculate_products_cost(self):
        """ Рассчет стоимости товаров """
        return self.records.aggregate(
            cost=Coalesce(models.Sum(
                models.F('order_price') * models.F('count'), output_field=ValuteField()
            ), 0)
        )['cost']

    @property
    def total_cost(self):
        """
            Метод получения полной стоимости заказа,
            которая может включать доставку / налог / ...
        """
        return self.products_cost

    def add_product(self, product, count=1):
        """
            Добавление товара в заказ.
            Метод предназначен для отладки. Реальные товары добавляются через корзину.
        """
        if isinstance(product, ShopProduct):
            pass
        else:
            product = ShopProduct.objects.get(id=product)

        try:
            ordered = self.records.get(product=product)
        except OrderRecord.DoesNotExist:
            order_product = OrderRecord(
                product=product,
                order_price=product.price,
                count=count,
            )
            self.records.add(order_product)
        else:
            ordered.count += count
            ordered.save()


class OrderRecord(models.Model):
    """ Продукты заказа """
    order = models.ForeignKey(ShopOrder, verbose_name=_('order'), related_name='records')
    product = models.ForeignKey(ShopProduct, verbose_name=_('product'), null=True, on_delete=models.SET_NULL)
    order_price = ValuteField(_('price per item'))
    count = models.PositiveIntegerField(_('quantity'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        unique_together = ('order', 'product')

    @property
    def total_cost(self):
        return self.order_price * self.count

    def __str__(self):
        product_name = self.product.title if self.product else _('Unknown')
        return '%s (x%s)' % (product_name, self.count)


class NotifyReceiver(models.Model):
    """ Получаети писем о новом оплаченном заказе """
    config = models.ForeignKey(ShopConfig, related_name='receivers')
    email = models.EmailField(_('e-mail'))

    class Meta:
        verbose_name = _('notify receiver')
        verbose_name_plural = _('notify receivers')

    def __str__(self):
        return self.email
