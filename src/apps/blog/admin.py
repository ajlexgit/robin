from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from suit.widgets import AutosizedTextarea
from libs.autocomplete.widgets import AutocompleteWidget
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from seo.admin import SeoModelAdminMixin
from .models import BlogConfig, BlogPost, Tag, PostTag


class BlogConfigForm(forms.ModelForm):
    class Meta:
        widgets = {
            'title': AutosizedTextarea(attrs={
                'class': 'input-xxlarge',
                'rows': 1,
            }),
        }


@admin.register(BlogConfig)
class BlogConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    form = BlogConfigForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-header'),
            'fields': ('title', ),
        }),
    )
    suit_form_tabs = (
        ('header', _('Header')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'


@admin.register(Tag)
class TagAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'alias'),
        }),
    )
    list_display = ('title',)
    prepopulated_fields = {'alias': ('title',)}


class PostTagForm(forms.ModelForm):
    class Meta:
        widgets = {
            'tag': AutocompleteWidget(
                minimum_input_length=0,
                expressions="title__icontains",
            )
        }


class PostTagAdmin(ModelAdminInlineMixin, admin.TabularInline):
    model = PostTag
    form = PostTagForm
    extra = 0
    suit_classes = 'suit-tab suit-tab-tags'


@admin.register(BlogPost)
class BlogPostAdmin(SeoModelAdminMixin, ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('preview', 'title', 'alias', 'status', 'date'),
        }),
        (_('Content'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('note', 'text'),
        }),
    )
    inlines = (PostTagAdmin, )
    list_display = ('view', 'title', 'tags_list', 'date_format', 'status')
    list_display_links = ('title',)
    list_filter = ('status', )
    search_fields = ('title',)
    actions = ('make_public_action', 'make_draft_action')
    prepopulated_fields = {'alias': ('title', )}

    suit_form_tabs = (
        ('general', _('General')),
        ('tags', _('Tags')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

    def tags_list(self, obj):
        tags = obj.tags.all()
        return ' / '.join((str(item.title) for item in tags))
    tags_list.short_description = _('tags')

    def date_format(self, obj):
        return dateformat.format(localtime(obj.date), settings.DATETIME_FORMAT)
    date_format.short_description = _('Publish date')
    date_format.admin_order_field = 'date'

    def make_public_action(self, request, queryset):
        queryset.update(status=BlogPost.STATUS_PUBLIC)
    make_public_action.short_description = 'Make public'


    def make_draft_action(self, request, queryset):
        queryset.update(status=BlogPost.STATUS_DRAFT)
    make_draft_action.short_description = 'Make draft'