from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import SimpleListFilter


class HierarchyFilter(SimpleListFilter):
    hierarchy_filter = True
    template = 'admin/hierarchy_filter.html'

    def value(self):
        return super().value() or None

    def get_branch_choices(self, value):
        return ()

    def get_branch(self):
        value = self.value()
        if value is None:
            yield {
                'selected': value is None,
                'query_string': '?{}='.format(self.parameter_name),
                'display': _('All'),
            }
            return

        choices = self.get_branch_choices(value) or ()
        for lookup, title in choices:
            yield {
                'selected': value == force_text(lookup),
                'query_string': '?{}={}'.format(self.parameter_name, lookup),
                'display': title,
            }

    def choices(self, cl):
        value = self.value()
        for lookup, title in self.lookup_choices:
            yield {
                'selected': value == force_text(lookup),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }
