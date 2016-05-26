from django.contrib.sitemaps import GenericSitemap
from main.models import MainPageConfig

mainpage = {
    'queryset': MainPageConfig.objects.all(),
    'date_field': 'updated',
}


site_sitemaps = {
    'main': GenericSitemap(mainpage, changefreq='daily', priority=1),
}
