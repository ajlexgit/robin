from django.http.response import Http404
from django.shortcuts import resolve_url
from seo import Seo
from libs.views import TemplateExView
from .models import ShopConfig, ShopCategory, ShopProduct


class IndexView(TemplateExView):
    template_name = 'shop/index.html'

    def get(self, request):
        config = ShopConfig.get_solo()

        # Breadcrumbs
        request.breadcrumbs.add(config.header)

        # SEO
        seo = Seo()
        seo.set_data(config, defaults={
            'title': config.header
        })
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'root_categories': ShopCategory.objects.root_categories(),
        })


class CategoryView(TemplateExView):
    template_name = 'shop/category.html'

    def get(self, request, *args, **kwargs):
        config = ShopConfig.get_solo()

        try:
            category = ShopCategory.objects.get(alias=kwargs['category_alias'], is_visible=True)
        except (ShopCategory.DoesNotExist, ShopCategory.MultipleObjectsReturned):
            raise Http404

        # Breadcrumbs
        request.breadcrumbs.add(config.header, resolve_url('shop:index'))
        for parent_category in category.get_ancestors():
            request.breadcrumbs.add(
                parent_category.title,
                resolve_url('shop:category', category_alias=parent_category.alias)
            )
        request.breadcrumbs.add(category.title)

        # SEO
        seo = Seo()
        seo.set_title(config, default=config.header)
        seo.set_data(category, defaults={
            'title': category.title
        })
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'category': category,
            'root_categories': ShopCategory.objects.root_categories(),
        })


class DetailView(TemplateExView):
    template_name = 'shop/detail.html'

    def get(self, request, *args, **kwargs):
        config = ShopConfig.get_solo()

        try:
            category = ShopCategory.objects.get(alias=kwargs['category_alias'], is_visible=True)
        except (ShopCategory.DoesNotExist, ShopCategory.MultipleObjectsReturned):
            raise Http404

        try:
            product = ShopProduct.objects.get(alias=kwargs['alias'], is_visible=True)
        except (ShopProduct.DoesNotExist, ShopProduct.MultipleObjectsReturned):
            raise Http404

        # Breadcrumbs
        request.breadcrumbs.add(config.header, resolve_url('shop:index'))
        for parent_category in category.get_ancestors(include_self=True):
            request.breadcrumbs.add(
                parent_category.title,
                resolve_url('shop:category', category_alias=parent_category.alias)
            )
        request.breadcrumbs.add(product.title)

        # SEO
        seo = Seo()
        seo.set_title(config, default=config.header)
        seo.set_title(category, default=category.title)
        seo.set_data(product, defaults={
            'title': product.title,
            'og_image': product.photo,
        })
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'category': category,
            'product': product,
        })

