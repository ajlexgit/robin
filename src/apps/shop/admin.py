from django import forms
from django.db import models
from django.contrib import admin
from django.utils.timezone import now
from django.db.models import F, Func, Value
from django.db.models.functions import Concat
from django.contrib.admin.utils import unquote
from django.utils.translation import ugettext_lazy as _
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from project.admin.filters import HierarchyFilter
from solo.admin import SingletonModelAdmin
from attachable_blocks import AttachedBlocksStackedInline
from seo.admin import SeoModelAdminMixin
from libs.mptt import *
from libs import admin_utils
from libs.autocomplete import AutocompleteWidget
from .models import ShopConfig, ShopCategory, ShopProduct, ShopOrder, NotificationReceiver
from .signals import products_changed, categories_changed


class ShopConfigBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки главной страницы """
    suit_classes = 'suit-tab suit-tab-blocks'


class ShopCategoryBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки страницы категории """
    suit_classes = 'suit-tab suit-tab-blocks'


class NotificationReceiverAdmin(ModelAdminInlineMixin, admin.TabularInline):
    """ Инлайн получателей уведомлений о новых заказах """
    model = NotificationReceiver
    extra = 0
    suit_classes = 'suit-tab suit-tab-notify'


@admin.register(ShopConfig)
class ShopConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
    inlines = (ShopConfigBlocksInline, NotificationReceiverAdmin)
    suit_form_tabs = (
        ('general', _('General')),
        ('notify', _('Notifications')),
        ('blocks', _('Blocks')),
    )


class ShopCategoryForm(forms.ModelForm):
    """ Форма категории """
    class Meta:
        model = ShopCategory
        fields = '__all__'
        widgets = {
            'parent': AutocompleteWidget(
                format_item=ShopCategory.autocomplete_item,
                attrs={
                    'style': 'width:50%',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """ Exclude self """
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(pk=self.instance.pk)


@admin.register(ShopCategory)
class ShopCategoryAdmin(SeoModelAdminMixin, SortableMPTTModelAdmin):
    """ Категория """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'parent',
            ),
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'slug', 'is_visible'
            ),
        }),
    )
    mptt_level_indent = 20
    form = ShopCategoryForm
    inlines = (ShopCategoryBlocksInline, )
    actions = ('action_hide', 'action_show')
    list_display = ('view', 'title', 'is_visible', 'product_count', 'total_product_count')
    list_display_links = ('title',)
    prepopulated_fields = {
        'slug': ('title',)
    }
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
    )

    def action_hide(self, request, queryset):
        descentants = queryset.get_descendants(include_self=True)
        descentants.filter(
            is_visible=True
        ).update(
            is_visible=False
        )
        descentants.update(total_product_count=0)
        categories_changed.send(self.model, categories=queryset, include_self=False)
    action_hide.short_description = _('Hide selected %(verbose_name_plural)s')

    def action_show(self, request, queryset):
        queryset.get_ancestors(include_self=True).filter(
            is_visible=False
        ).update(
            is_visible=True
        )

        categories_changed.send(self.model, categories=queryset)
    action_show.short_description = _('Show selected %(verbose_name_plural)s')


class ShopProductCategoryFilter(HierarchyFilter):
    """ Фильтр продуктов по категории """
    title = _('Category')
    parameter_name = 'category'

    def get_branch_choices(self, value):
        try:
            category = ShopCategory.objects.get(pk=value)
        except ShopCategory.DoesNotExist:
            return ()
        else:
            return category.get_ancestors(include_self=True).values_list('id', 'title')

    def lookups(self, request, model_admin):
        value = self.value()
        if value:
            subcategs = ShopCategory.objects.filter(parent=value).values_list('id', 'title')
            if subcategs:
                return subcategs
            else:
                categ = ShopCategory.objects.get(pk=value)
                return ShopCategory.objects.filter(parent=categ.parent).values_list('id', 'title')
        else:
            return ShopCategory.objects.root_categories().values_list('id', 'title')

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            category = ShopCategory.objects.filter(pk=value)
            categories = ShopCategory.objects.get_queryset_descendants(category, include_self=True)
            queryset = queryset.filter(category__in=categories).distinct()
        return queryset


class ShopProductForm(forms.ModelForm):
    """ Форма продукта """
    class Meta:
        model = ShopProduct
        fields = '__all__'
        widgets = {
            'category': AutocompleteWidget(
                format_item=ShopCategory.autocomplete_item,
                attrs={
                    'style': 'width:50%',
                }
            )
        }


@admin.register(ShopProduct)
class ShopProductAdmin(SeoModelAdminMixin, admin.ModelAdmin):
    """ Продукт """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'category', 'title', 'slug', 'price', 'is_visible',
            ),
        }),
        (_('Additional information'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'gallery', 'description',
            ),
        }),
    )
    form = ShopProductForm
    actions = ('action_hide', 'action_show')
    search_fields = ('title', 'category__title')
    list_display = (
        'view', 'micropreview', '__str__', 'category_link',
        'price_alternative', 'is_visible',
    )
    list_display_links = ('micropreview', '__str__', )
    list_filter = (ShopProductCategoryFilter, )
    prepopulated_fields = {
        'slug': ('title', ),
    }
    suit_form_tabs = (
        ('general', _('General')),
    )

    def suit_cell_attributes(self, obj, column):
        """ Классы для ячеек списка """
        default = super().suit_cell_attributes(obj, column)
        if column == 'micropreview':
            default.setdefault('class', '')
            default['class'] += ' mini-column'
        return default

    def micropreview(self, obj):
        if not obj.photo:
            return '-//-'
        return '<img src="{}" width="{}" height="{}">'.format(
            obj.photo.admin_micro.url,
            obj.photo.admin_micro.target_width,
            obj.photo.admin_micro.target_height,
        )
    micropreview.short_description = _('Preview')
    micropreview.allow_tags = True

    def category_link(self, obj):
        meta = getattr(obj.category, '_meta')
        return '<a href="{0}">{1}</a>'.format(
            admin_utils.get_change_url(meta.app_label, meta.model_name, obj.category.pk),
            obj.category
        )
    category_link.short_description = _('Categories')
    category_link.allow_tags = True

    def price_alternative(self, obj):
        return '<nobr>%s</nobr>' % obj.price.alternative
    price_alternative.allow_tags = True
    price_alternative.admin_order_field = 'price'
    price_alternative.short_description = _('Price')

    def action_hide(self, request, queryset):
        queryset.update(is_visible=False)
        categories = queryset.values_list(
            'category_id', flat=True
        )
        products_changed.send(self.model, categories=categories)
    action_hide.short_description = _('Hide selected %(verbose_name_plural)s')

    def action_show(self, request, queryset):
        queryset.update(is_visible=True)
        categories = queryset.values_list(
            'category_id', flat=True
        )
        products_changed.send(self.model, categories=categories)
    action_show.short_description = _('Show selected %(verbose_name_plural)s')


class StatusShopOrderFilter(HierarchyFilter):
    """ Фильтр заказов по статусу """
    title = _('Status')
    parameter_name = 'status'

    STATUSES = (
        ('all', _('All')),
        ('non_checked', _('Not checked')),
        ('checked', _('Checked')),
        ('paid', _('Paid')),
        ('cancelled', _('Cancelled')),
        ('archived', _('Archived')),
    )

    def value(self):
        value = super().value()
        if value is None:
            value = 'non_checked'
        return value

    def lookups(self, request, model_admin):
        result = []
        for key, name in self.STATUSES:
            qs = self.queryset(request, model_admin.model._default_manager, key)
            result.append((key, '%s (%d)' % (name, qs.count())))

        return result

    def get_branch_choices(self, value):
        return [
            (value, dict(self.STATUSES).get(value))
        ]

    def queryset(self, request, queryset, value=None):
        value = value or self.value()
        if value == 'non_checked':
            queryset = queryset.filter(
                confirmed=True, checked=False, paid=None, archived=False, cancelled=False
            )
        elif value == 'checked':
            queryset = queryset.filter(
                confirmed=True, checked=True, paid=False, archived=False, cancelled=False
            )
        elif value == 'paid':
            queryset = queryset.filter(
                confirmed=True, checked=True, paid=True, archived=False, cancelled=False
            )
        elif value == 'cancelled':
            queryset = queryset.filter(
                confirmed=True, checked=None, paid=None, archived=False, cancelled=True
            )
        elif value == 'archived':
            queryset = queryset.filter(
                confirmed=True, checked=None, paid=None, archived=True, cancelled=None
            )
        return queryset


class ShopOrderForm(forms.ModelForm):
    """ Форма заказа """
    DATED_FLAGS = (
        ('is_confirmed', 'confirm_date'),
        ('is_cancelled', 'cancel_date'),
        ('is_checked', 'check_date'),
        ('is_paid', 'pay_date'),
        ('is_archived', 'archivation_date'),
    )

    class Meta:
        model = ShopOrder
        fields = '__all__'

    def _set_date(self, value, flagname, datename):
        if value and not getattr(self.instance, flagname):
            setattr(self.instance, datename, now())
        elif not value:
            setattr(self.instance, datename, None)

    def clean(self):
        data = super().clean()
        for flagname, datename in self.DATED_FLAGS:
            value = data.get(flagname)
            if value is not None:
                self._set_date(value, flagname, datename)
        return data


@admin.register(ShopOrder)
class ShopOrderAdmin(ModelAdminMixin, admin.ModelAdmin):
    """ Заказ """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'created',
            ),
        }),

        (_('Confirmed by user'), {
            'classes': ('suit-tab', 'suit-tab-status'),
            'fields': (
                'is_confirmed', 'confirm_date',
            ),
        }),
        (_('Checked'), {
            'classes': ('suit-tab', 'suit-tab-status'),
            'fields': (
                'is_checked', 'check_date',
            ),
        }),
        (_('Cancelled'), {
            'classes': ('suit-tab', 'suit-tab-status'),
            'fields': (
                'is_cancelled', 'cancel_date',
            ),
        }),
        (_('Paid'), {
            'classes': ('suit-tab', 'suit-tab-status'),
            'fields': (
                'is_paid', 'pay_date',
            ),
        }),
        (_('Archived'), {
            'classes': ('suit-tab', 'suit-tab-status'),
            'fields': (
                'is_archived', 'archivation_date',
            ),
        }),
    )
    form = ShopOrderForm
    date_hierarchy = 'created'
    readonly_fields = (
        'products_cost', 'fmt_total_cost', 'created',
        'is_confirmed', 'confirm_date',
        'cancel_date', 'check_date', 'pay_date', 'archivation_date',
    )
    list_display = (
        '__str__', 'fmt_total_cost', 'is_cancelled', 'is_checked', 'is_paid', 'pay_date', 'created',
    )
    actions = ('action_set_checked', 'action_set_cancelled', 'action_set_paid', 'action_set_archived')
    list_filter = (StatusShopOrderFilter,)
    suit_form_tabs = (
        ('general', _('General')),
        ('products', _('Products')),
        ('status', _('Status')),
    )
    suit_form_includes = (
        ('shop/admin/products.html', 'top', 'products'),
    )

    def suit_row_attributes(self, obj, request):
        if obj.is_cancelled:
            return {'class': 'error'}
        if obj.is_paid:
            return {'class': 'success'}

    def fmt_total_cost(self, obj):
        return obj.total_cost.alternative
    fmt_total_cost.short_description = _('Total cost')
    fmt_total_cost.admin_order_field = 'products_cost'

    def has_add_permission(self, request):
        return False

    def action_set_checked(self, request, queryset):
        queryset.update(is_checked=True)
    action_set_checked.short_description = _('Set %(verbose_name_plural)s checked')

    def action_set_paid(self, request, queryset):
        queryset.update(is_paid=True)
    action_set_paid.short_description = _('Set %(verbose_name_plural)s paid')

    def action_set_cancelled(self, request, queryset):
        queryset.update(is_cancelled=True)
    action_set_cancelled.short_description = _('Set %(verbose_name_plural)s cancelled')

    def action_set_archived(self, request, queryset):
        queryset.update(is_archived=True)
    action_set_archived.short_description = _('Set %(verbose_name_plural)s archived')

    def change_view(self, request, object_id, *args, **kwargs):
        if object_id is None:
            entity = None
        else:
            entity = self.get_object(request, unquote(object_id))

        extra_context = kwargs.pop('extra_context', None) or {}
        kwargs['extra_context'] = dict(extra_context, **{
            'entity': entity,
        })
        return super().change_view(request, object_id, *args, **kwargs)
