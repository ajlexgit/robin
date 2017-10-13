from django.contrib import admin #добавляем админку
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from suit.admin import SortableModelAdmin
from project.admin import ModelAdminMixin
from .models import RobinPageConfig, Subscribes, Student, Test


@admin.register(RobinPageConfig)
class RobinPageConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (

            ),
        }),
    )
    
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
    )


@admin.register(Subscribes)
class SubscribesAdmin(ModelAdminMixin, SortableModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'email', 'name', 'thirdname', 'nua',
            ),
        }),
    )
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
    )

@admin.register(Test)
class TestAdmin(ModelAdminMixin, SortableModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'email', 'name', 'thirdname', 'nua',
            ),
        }),
    )
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
    )


@admin.register(Student)
class StudentAdmin(ModelAdminMixin, SortableModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'freshman', 'sophomore', 'junior', 'senior',
            ),
        }),
    )
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
    )