from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from comments.admin import CommentsModelAdminMixin
from attachable_blocks import AttachableBlockRefTabularInline
from .models import MainPageConfig, MainBlockFirst, MainBlockSecond, InlineSample, ListItem


class InlineSampleAdmin(admin.TabularInline):
    model = InlineSample
    extra = 0
    suit_classes = 'suit-tab suit-tab-general'


class MyPageBlockRefInline(AttachableBlockRefTabularInline):
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(MainBlockFirst)
class MainBlockFirstAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')


@admin.register(MainBlockSecond)
class MainBlockSecondAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')


@admin.register(MainPageConfig)
class MainPageConfigAdmin(CommentsModelAdminMixin, SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (_('Header'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header_title', 'header_background', 'header_video',
            ),
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'preview', 'preview2', 'text', 'description',
                'color', 'color2' ,'price', 'gallery', 'video'
            ),
        }),
    )
    inlines = (InlineSampleAdmin, MyPageBlockRefInline)
    suit_form_tabs = (
        ('general', _('General')),
        ('comments', _('Comments')),
        ('blocks', _('Blocks')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'
    suit_comments_position = 'bottom'
    suit_comments_tab = 'comments'


class StatusListItemFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'
    template = 'admin/button_filter.html'

    def value(self):
        value = super().value()
        return value or None

    def lookups(self, request, model_admin):
        return ListItem.STATUSES

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset = queryset.filter(status__in=value)
        return queryset


@admin.register(ListItem)
class ListItemAdmin(ModelAdminMixin, admin.ModelAdmin):
    list_display = ('view', 'title', 'status')
    list_display_links = ('title', )
    list_filter = (StatusListItemFilter, )