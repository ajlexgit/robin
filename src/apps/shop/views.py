from django.http.response import Http404
from seo import Seo
from libs.views import TemplateExView
from .models import ShopConfig, ShopCategory, ShopProduct


class IndexView(TemplateExView):
    config = None
    template_name = 'shop/index.html'

    def before_get(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()

    def get(self, request):
        # Breadcrumbs
        request.breadcrumbs.add(self.config.title)

        # SEO
        seo = Seo()
        seo.set_data(self.config, defaults={
            'title': self.config.header
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'root_categories': ShopCategory.objects.root_categories(),
        })


class CategoryView(TemplateExView):
    config = None
    category = None
    template_name = 'shop/category.html'

    def before_get(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()

        try:
            self.category = ShopCategory.objects.get(alias=kwargs['category_alias'])
        except (ShopCategory.DoesNotExist, ShopCategory.MultipleObjectsReturned):
            raise Http404

    def get(self, request, *args, **kwargs):
        if not self.category.is_visible:
            raise Http404

        # Breadcrumbs
        request.breadcrumbs.add(self.config.header, 'shop:index')
        parent_categories = self.category.get_ancestors()
        for category in parent_categories:
            request.breadcrumbs.add(category.title, 'shop:category', category_alias=category.alias)
        request.breadcrumbs.add(self.category.title)

        # SEO
        seo = Seo()
        seo.set_title(self.config, default=self.config.header)
        seo.set_data(self.category, defaults={
            'title': self.category.title
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'current_category': self.category,
            'root_categories': ShopCategory.objects.root_categories(),
        })


class DetailView(TemplateExView):
    config = None
    product = None
    category = None
    template_name = 'shop/detail.html'

    def before_get(self, request, *args, **kwargs):
        self.config = ShopConfig.get_solo()

        try:
            self.category = ShopCategory.objects.get(alias=kwargs['category_alias'])
        except (ShopCategory.DoesNotExist, ShopCategory.MultipleObjectsReturned):
            raise Http404

        try:
            self.product = ShopProduct.objects.get(alias=kwargs['alias'])
        except (ShopProduct.DoesNotExist, ShopProduct.MultipleObjectsReturned):
            raise Http404

    def get(self, request, *args, **kwargs):
        if not self.category.is_visible or not self.product.is_visible:
            raise Http404

        # Breadcrumbs
        request.breadcrumbs.add(self.config.header, 'shop:index')
        parent_categories = self.category.get_ancestors(include_self=True)
        for category in parent_categories:
            request.breadcrumbs.add(category.title, 'shop:category', category_alias=category.alias)
        request.breadcrumbs.add(self.product.title)

        # SEO
        seo = Seo()
        seo.set_title(self.config, default=self.config.header)
        seo.set_title(self.category, default=self.category.title)
        seo.set_data(self.product, defaults={
            'title': self.product.title,
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'current_category': self.category,
            'current_product': self.product,
        })

