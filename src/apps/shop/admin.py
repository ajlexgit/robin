from django import forms
from django.db import models
from django.contrib import admin
from django.db.models import F, Func, Value
from django.core.urlresolvers import reverse
from django.db.models.functions import Concat
from django.contrib.admin.utils import unquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import SimpleListFilter
from project.admin import ModelAdminMixin
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from libs.mptt import *
from libs.autocomplete.forms import AutocompleteField
from .models import ShopConfig, ShopCategory, ShopProduct, ShopOrder


@admin.register(ShopConfig)
class ShopConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title',
            ),
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'


@admin.register(ShopCategory)
class ShopCategoryAdmin(SeoModelAdminMixin, ModelAdminMixin, SortableMPTTModelAdmin):
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
                'title', 'alias', 'is_visible'
            ),
        }),
    )
    mptt_level_indent = 20
    actions = ('make_hidden', 'make_visible')
    list_display = ('view', 'title', 'is_visible', 'product_count')
    list_display_links = ('title',)
    prepopulated_fields = {'alias': ('title',)}
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

    def make_hidden(self, request, queryset):
        queryset.update(is_visible=False)
        self.model.objects.get_queryset_descendants(queryset).filter(
            is_visible=True
        ).update(
            is_visible=False
        )
    make_hidden.short_description = _('Hide selected %(verbose_name_plural)s')

    def make_visible(self, request, queryset):
        queryset.update(is_visible=True)
        self.model.objects.get_queryset_ancestors(queryset).filter(
            is_visible=False
        ).update(
            is_visible=True
        )
    make_visible.short_description = _('Show selected %(verbose_name_plural)s')


class StatusShopProductCategoryFilter(SimpleListFilter):
    """ Фильтр по категории """
    title = _('Category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return ShopCategory.objects.annotate(
            text=Concat(
                Func(
                    Value('–'),
                    F('level'),
                    function='REPEAT',
                    output_field=models.CharField()
                ),
                F('title'),
            )
        ).values_list('id', 'text')

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            category = ShopCategory.objects.filter(pk=value)
            categories = ShopCategory.objects.get_queryset_descendants(category, include_self=True)
            queryset = queryset.filter(category__in=categories).distinct()
        return queryset


class ShopProductForm(forms.ModelForm):
    category = AutocompleteField(
        label=ShopProduct._meta.get_field('category').verbose_name.capitalize(),
        queryset=ShopCategory.objects.all(),
        expressions="title__icontains",
        item2dict_func=ShopCategory.autocomplete_item,
        minimum_input_length=0,
        widget_width='50%',
    )

    class Meta:
        model = ShopProduct
        fields = '__all__'


@admin.register(ShopProduct)
class ShopProductAdmin(SeoModelAdminMixin, ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'category', 'title', 'alias', 'serial', 'photo', 'price',
                'is_visible', 'description',
            ),
        }),
    )
    form = ShopProductForm
    actions = ('make_hidden', 'make_visible')
    list_display = (
        'view', 'micropreview', '__str__', 'serial', 'category_link',
        'price_alternate', 'is_visible',
    )
    search_fields = ('title', 'category__title')
    list_display_links = ('micropreview', '__str__', )
    list_filter = (StatusShopProductCategoryFilter, )
    prepopulated_fields = {
        'alias': ('title', ),
        'serial': ('title', ),
    }
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

    def micropreview(self, obj):
        if not obj.photo:
            return '-//-'
        return '<img src="{}">'.format(obj.photo.admin_micro.url)
    micropreview.short_description = _('Preview')
    micropreview.allow_tags = True

    def category_link(self, obj):
        url = reverse('admin:shop_shopcategory_change', args=(obj.pk, ))
        return '<a href="{0}">{1}</a>'.format(url, obj.category)
    category_link.short_description = _('Category')
    category_link.allow_tags = True

    def price_alternate(self, obj):
        return '<nobr>%s</nobr>' % obj.price.alternate
    price_alternate.allow_tags = True
    price_alternate.short_description = _('Price')

    def make_hidden(self, request, queryset):
        queryset.update(is_visible=False)
        categories = ShopCategory.objects.filter(
            pk__in=queryset.values_list(
                'category_id', flat=True
            ).distinct().order_by('category_id')
        )
        ShopCategory.objects.reset_product_count(leaf_queryset=categories)

    make_hidden.short_description = _('Hide selected %(verbose_name_plural)s')

    def make_visible(self, request, queryset):
        queryset.update(is_visible=True)
        categories = ShopCategory.objects.filter(
            pk__in=queryset.values_list(
                'category_id', flat=True
            ).distinct().order_by('category_id')
        )
        ShopCategory.objects.reset_product_count(leaf_queryset=categories)
    make_visible.short_description = _('Show selected %(verbose_name_plural)s')


class StatusShopOrderFilter(SimpleListFilter):
    """ Фильтр по статусу """
    title = _('Status')
    parameter_name = 'status'
    template = 'admin/button_filter.html'

    def lookups(self, request, model_admin):
        return ShopOrder.STATUS

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset = queryset.filter(status=value)
        return queryset


@admin.register(ShopOrder)
class ShopOrderAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (_('Cost'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('fmt_products_cost', 'fmt_total_cost', ),
        }),
        (_('Status'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'status', 'date', 'pay_date',
            ),
        }),
    )
    date_hierarchy = 'date'
    readonly_fields = (
        'fmt_products_cost', 'fmt_total_cost', 'date', 'pay_date',
    )
    list_display = (
        '__str__', 'status', 'fmt_total_cost', 'date', 'pay_date',
    )
    list_filter = (StatusShopOrderFilter, 'date')
    suit_form_tabs = (
        ('general', _('General')),
        ('products', _('Products')),
    )
    suit_form_includes = (
        ('shop/admin/products.html', 'top', 'products'),
    )

    def fmt_products_cost(self, obj):
        return obj.products_cost.alternate
    fmt_products_cost.short_description = _('Products cost')
    fmt_products_cost.admin_order_field = 'products_cost'

    def fmt_total_cost(self, obj):
        return obj.total_cost.alternate
    fmt_total_cost.short_description = _('Total cost')

    def has_add_permission(self, request):
        return False

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
