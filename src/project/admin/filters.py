from django.contrib.admin.filters import SimpleListFilter


class HierarchyFilter(SimpleListFilter):
    hierarchy_filter = True
    template = 'admin/hierarchy_filter.html'
