from django import forms
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.utils import unquote
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from suit.admin import SortableModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from mptt.admin import MPTTModelAdmin
from libs.autocomplete.forms import AutocompleteMultipleField
from .models import ShopConfig, Category, Product, Order


@admin.register(ShopConfig)
class ShopConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (

    )
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'


@admin.register(Category)
class CategoryAdmin(SeoModelAdminMixin, ModelAdminMixin, MPTTModelAdmin, SortableModelAdmin):
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
    list_display = ('view', 'title', 'is_visible')
    list_display_links = ('title',)
    prepopulated_fields = {'alias': ('title',)}
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

    def make_hidden(modeladmin, request, queryset):
        queryset.update(visible=False)
    make_hidden.short_description = _('Make hidden')

    def make_visible(modeladmin, request, queryset):
        queryset.update(visible=True)
    make_visible.short_description = _('Make visible')


class ProductForm(forms.ModelForm):
    categories = AutocompleteMultipleField(
        label=Product._meta.get_field('categories').verbose_name.capitalize(),
        queryset=Category.objects.all(),
        expressions="title__icontains",
        minimum_input_length=0,
    )

    class Meta:
        model = Product


@admin.register(Product)
class ProductAdmin(SeoModelAdminMixin, ModelAdminMixin, SortableModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'alias', 'serial', 'categories', 'photo',
                'description', 'price', 'is_visible',
            ),
        }),
    )
    form = ProductForm
    actions = ('make_hidden', 'make_visible')
    list_filter = ('categories', )
    list_display = ('view', '__str__', 'serial', 'categories_list', 'price_alternate', 'is_visible')
    list_display_links = ('__str__', )
    prepopulated_fields = {'alias': ('title', )}
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

    def categories_list(self, obj):
        return ', '.join(
            item.title
            for item in obj.categories.all()
        )
    categories_list.short_description = _('Categories')

    def price_alternate(self, obj):
        return obj.price.alternate
    price_alternate.short_description = _('Price')
    price_alternate.admin_order_field = 'price'

    def make_hidden(modeladmin, request, queryset):
        queryset.update(visible=False)
    make_hidden.short_description = _('Make hidden')

    def make_visible(modeladmin, request, queryset):
        queryset.update(visible=True)
    make_visible.short_description = _('Make visible')


class StatusOrderFilter(SimpleListFilter):
    """ Фильтр по статусу """
    title = _('Status')
    parameter_name = 'status'
    template = 'admin/button_filter.html'

    def lookups(self, request, model_admin):
        return Order.STATUS

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset = queryset.filter(status=value)
        return queryset


@admin.register(Order)
class OrderAdmin(ModelAdminMixin, admin.ModelAdmin):
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
    list_filter = (StatusOrderFilter, 'date')
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
