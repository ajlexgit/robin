from django.dispatch import receiver
from libs.views import TemplateExView
from .models import ShopConfig, ShopCategory, ShopProduct, ShopOrder
from .signals import order_payed


class IndexView(TemplateExView):
    template_name = 'shop/index.html'

    def get_objects(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()

    def get(self, request):
        # Breadcrumbs
        request.breadcrumbs.add(self.config.title)

        # SEO
        request.seo.set_instance(self.config)

        return self.render_to_response({
            'config': self.config,
            'root_categories': ShopCategory.objects.root_categories(),
        })


class CategoryView(TemplateExView):
    template_name = 'shop/category.html'

    def get_objects(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()
        self.category = ShopCategory.objects.get(alias=kwargs['category_alias'])

    def get(self, request, *args, **kwargs):
        # Breadcrumbs
        request.breadcrumbs.add(self.config.title, 'shop:index')
        parent_categories = self.category.get_ancestors()
        for category in parent_categories:
            request.breadcrumbs.add(self.config.title, 'shop:category', category_alias=category.alias)
        request.breadcrumbs.add(self.category.title)

        # SEO
        request.seo.set_instance(self.category)

        return self.render_to_response({
            'config': self.config,
            'current_category': self.category,
            'root_categories': ShopCategory.objects.root_categories(),
        })


class DetailView(TemplateExView):
    template_name = 'shop/detail.html'

    def get_objects(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()
        self.category = ShopCategory.objects.get(alias=kwargs['category_alias'])
        self.product = ShopProduct.objects.get(alias=kwargs['alias'])

    def get(self, request, *args, **kwargs):
        # SEO
        request.seo.set_instance(self.product)

        return self.render_to_response({
            'config': self.config,
            'current_category': self.category,
            'current_product': self.product,
        })


@receiver(order_payed, sender=ShopOrder)
def order_payed(sender, **kwargs):
    """ Обработчик сигнала оплаты заказа """
    order = kwargs.get('order')
    if not order or not isinstance(order, ShopOrder):
        return

    order.mark_payed()