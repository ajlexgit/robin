from django.contrib.sitemaps import GenericSitemap
from main.models import MainPageConfig

mainpage_dict = {
    'queryset': MainPageConfig.objects.all(),
    'date_field': 'updated',
}


site_sitemaps = {
    'main': GenericSitemap(mainpage_dict, changefreq='weekly', priority=0.5),
}
