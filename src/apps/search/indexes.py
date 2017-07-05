from libs.sphinx.index import SphinxScheme, SphinxXMLIndex
from shop.models import ShopProduct


class SearchScheme(SphinxScheme):
    def __init__(self, index_name):
        super().__init__(index_name)
        self.add_fields('title', is_attribute=True)
        self.add_fields('description')
        self.add_attr('url')


class ShopProductsIndex(SphinxXMLIndex):
    name = 'shop_products'
    model = ShopProduct
    scheme_class = SearchScheme

    def get_queryset(self):
        return self.model.objects.filter(visible=True)

    def build_document(self, instance):
        return {
            'url': instance.get_absolute_url(),
            'title': instance.title,
            'description': instance.description,
        }
