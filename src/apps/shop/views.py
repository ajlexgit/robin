from django.dispatch import receiver
from django.http.response import Http404
from libs.views import TemplateExView
from .models import ShopConfig, Category, Product, Order
from .signals import order_payed


class IndexView(TemplateExView):
    template_name = 'shop/index.html'

    def get_objects(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()

    def get(self, request):
        categories = Category.objects.filter(visible=True).distinct()
        if not categories:
            raise Http404

        # SEO
        request.seo.set_instance(self.config)

        return self.render_to_response({
            'config': self.config,
            'categories': categories,
        })


class CategoryView(TemplateExView):
    template_name = 'shop/category.html'

    def get_objects(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()
        self.category = Category.objects.get(alias=kwargs['alias'])

    def get(self, request, *args, **kwargs):
        # SEO
        request.seo.set_instance(self.category)

        return self.render_to_response({
            'config': self.config,
            'category': self.category,
        })


class DetailView(TemplateExView):
    template_name = 'shop/detail.html'

    def get_objects(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()
        self.category = Category.objects.get(alias=kwargs['category_alias'])
        self.product = Product.objects.get(alias=kwargs['alias'])

    def get(self, request, *args, **kwargs):
        # SEO
        request.seo.set_instance(self.product)

        return self.render_to_response({
            'config': self.config,
            'category': self.category,
            'product': self.product,
        })


@receiver(order_payed, sender=Order)
def order_payed(sender, **kwargs):
    """ Обработчик сигнала оплаты заказа """
    order = kwargs.get('order')
    if not order or not isinstance(order, Order):
        return

    order.mark_payed()