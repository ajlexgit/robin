from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from attachable_blocks.admin import AttachedBlocksStackedInline
from seo.admin import SeoModelAdminMixin
from social_networks.admin import AutoPostMixin
from libs.autocomplete import AutocompleteWidget
from .models import BlogConfig, BlogPost, Tag, PostTag


class BlogConfigBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(BlogConfig)
class BlogConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('header', ),
        }),
        (_('Schema.org defaults'), {
            'classes': ('suit-tab', 'suit-tab-seo'),
            'fields': (
                'microdata_author', 'microdata_publisher_logo',
            ),
        }),
    )
    inlines = (BlogConfigBlocksInline, )
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
    )


@admin.register(Tag)
class TagAdmin(ModelAdminMixin, admin.ModelAdmin):
    """ Тэг """
    fieldsets = (
        (None, {
            'fields': ('title', 'slug'),
        }),
    )
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class PostTagForm(forms.ModelForm):
    """ Форма связи тэга и поста """
    class Meta:
        widgets = {
            'tag': AutocompleteWidget(
                minimum_input_length=0,
                expressions="title__icontains",
            )
        }


class PostTagAdmin(ModelAdminInlineMixin, admin.TabularInline):
    """ Инлайн тэгов поста """
    model = PostTag
    form = PostTagForm
    extra = 0
    suit_classes = 'suit-tab suit-tab-tags'


@admin.register(BlogPost)
class BlogPostAdmin(SeoModelAdminMixin, AutoPostMixin, admin.ModelAdmin):
    """ Пост """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('preview', 'header', 'slug', 'status', 'date'),
        }),
        (_('Content'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('note', 'text'),
        }),
    )
    inlines = (PostTagAdmin, )
    list_display = ('view', '__str__', 'tags_list', 'date_fmt', 'status')
    list_display_links = ('__str__',)
    list_filter = ('status',)
    search_fields = ('title',)
    actions = ('make_public_action', 'make_draft_action')
    prepopulated_fields = {'slug': ('header', )}

    suit_form_tabs = (
        ('general', _('General')),
        ('tags', _('Tags')),
    )

    def tags_list(self, obj):
        return ' / '.join((str(item.title) for item in obj.tags.all()))
    tags_list.short_description = _('tags')

    def date_fmt(self, obj):
        return dateformat.format(localtime(obj.date), settings.DATETIME_FORMAT)
    date_fmt.short_description = _('Publication date')
    date_fmt.admin_order_field = 'date'

    def get_autopost_text(self, obj):
        return obj.note

    def make_public_action(self, request, queryset):
        queryset.update(status=self.model.STATUS_PUBLIC)
    make_public_action.short_description = _('Make public')

    def make_draft_action(self, request, queryset):
        queryset.update(status=self.model.STATUS_DRAFT)
    make_draft_action.short_description = _('Make draft')
