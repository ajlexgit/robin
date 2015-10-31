from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from seo.admin import SeoModelAdminMixin
from suit.admin import SortableStackedInline
from files.admin import PageFileInlineMixin
from comments.admin import CommentsModelAdminMixin
from attachable_blocks import AttachedBlocksTabularInline
from .models import MainPageConfig, MainBlockFirst, MainBlockSecond, InlineSample, ListItem, ListItemFile


class InlineSampleAdmin(ModelAdminInlineMixin, admin.TabularInline):
    model = InlineSample
    extra = 0
    suit_classes = 'suit-tab suit-tab-general'


class MyPageFirstBlocksInline(AttachedBlocksTabularInline):
    set_name = 'first'
    verbose_name = 'My first block'
    verbose_name_plural = 'My first blocks'
    suit_classes = 'suit-tab suit-tab-blocks'


class MyPageSecondBlocksInline(AttachedBlocksTabularInline):
    set_name = 'second'
    verbose_name = 'My second block'
    verbose_name_plural = 'My second blocks'
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
                'color', 'color2' ,'price', 'coords', 'coords2', 'gallery', 'video'
            ),
        }),
    )
    inlines = (InlineSampleAdmin, MyPageFirstBlocksInline, MyPageSecondBlocksInline)
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


class ListItemFileInline(PageFileInlineMixin, SortableStackedInline):
    model = ListItemFile
    suit_classes = 'suit-tab suit-tab-files'


@admin.register(ListItem)
class ListItemAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'status', 'text',
            ),
        }),
    )
    inlines = (ListItemFileInline, )
    list_display = ('view', 'title', 'status')
    list_display_links = ('title', )
    list_filter = (StatusListItemFilter, )

    suit_form_tabs = (
        ('general', _('General')),
        ('files', _('Files')),
    )
