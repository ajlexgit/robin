from django.dispatch import receiver
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from libs.views import TemplateExView
from .models import ShopConfig, Category, Product, Order
from .signals import order_payed


class IndexView(TemplateExView):
    template_name = 'shop/index.html'

    def get(self, request):
        config = ShopConfig.get_solo()

        categories = Category.objects.filter(visible=True).distinct()
        if not categories:
            raise Http404

        # SEO
        request.seo.set_instance(config)

        return self.render_to_response({
            'config': config,
            'categories': categories,
        })


class CategoryView(TemplateExView):
    template_name = 'shop/category.html'

    def get(self, request, alias):
        config = ShopConfig.get_solo()
        category = get_object_or_404(Category, alias=alias)

        # SEO
        request.seo.set_instance(category)

        return self.render_to_response({
            'config': config,
            'category': category,
        })


class DetailView(TemplateExView):
    template_name = 'shop/detail.html'

    def get(self, request, category_alias, alias):
        config = ShopConfig.get_solo()
        category = get_object_or_404(Category, alias=category_alias)
        product = get_object_or_404(Product, alias=alias)

        # SEO
        request.seo.set_instance(product)

        return self.render_to_response({
            'config': config,
            'category': category,
            'product': product,
        })


@receiver(order_payed, sender=Order)
def order_payed(sender, **kwargs):
    """ Обработчик сигнала оплаты заказа """
    order = kwargs.get('order')
    if not order or not isinstance(order, Order):
        return

    order.mark_payed()