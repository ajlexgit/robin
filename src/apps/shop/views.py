from django.shortcuts import resolve_url
from django.http.response import Http404
from django.views.generic import TemplateView
from seo import Seo
from .models import ShopConfig, ShopCategory, ShopProduct


class IndexView(TemplateView):
    template_name = 'shop/index.html'

    def get(self, request, *args, **kwargs):
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


class CategoryView(TemplateView):
    template_name = 'shop/category.html'

    def get(self, request, *args, **kwargs):
        config = ShopConfig.get_solo()

        try:
            category = ShopCategory.objects.get(slug=kwargs['category_slug'], is_visible=True)
        except (ShopCategory.DoesNotExist, ShopCategory.MultipleObjectsReturned):
            raise Http404

        # Breadcrumbs
        request.breadcrumbs.add(config.header, resolve_url('shop:index'))
        for parent_category in category.get_ancestors():
            request.breadcrumbs.add(
                parent_category.title,
                resolve_url('shop:category', category_slug=parent_category.slug)
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


class DetailView(TemplateView):
    template_name = 'shop/detail.html'

    def get(self, request, *args, **kwargs):
        config = ShopConfig.get_solo()

        try:
            category = ShopCategory.objects.get(slug=kwargs['category_slug'], is_visible=True)
        except (ShopCategory.DoesNotExist, ShopCategory.MultipleObjectsReturned):
            raise Http404

        try:
            product = ShopProduct.objects.get(slug=kwargs['slug'], is_visible=True)
        except (ShopProduct.DoesNotExist, ShopProduct.MultipleObjectsReturned):
            raise Http404

        # Breadcrumbs
        request.breadcrumbs.add(config.header, resolve_url('shop:index'))
        for parent_category in category.get_ancestors(include_self=True):
            request.breadcrumbs.add(
                parent_category.title,
                resolve_url('shop:category', category_slug=parent_category.slug)
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
