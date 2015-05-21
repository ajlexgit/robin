from django.contrib.sitemaps import Sitemap
from main.models import MainPageConfig


class MainPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return MainPageConfig.objects.all()

    def lastmod(self, obj):
        return obj.updated


site_sitemaps = {
    'main': MainPageSitemap,
}