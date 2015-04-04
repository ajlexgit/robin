from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from project.admin import ModelAdminMixin
from libs.widgets import SplitDateTimeWidget
from libs.autocomplete import AutocompleteField, AutocompleteMultipleField
from files.admin import PageFileInline
from comments.admin import CommentsModelAdminMixin
from .models import *


class PostFileInline(PageFileInline):
    model = PostFile
    suit_classes = 'suit-tab suit-tab-general'


class PostAdminForm(forms.ModelForm):
    sections = AutocompleteMultipleField(
        label=Post.sections.field.verbose_name.capitalize(),
        queryset=PostSection.objects.all(),
        minimum_input_length=0,
    )

    author = AutocompleteField(
        label=Post.author.field.verbose_name.capitalize(),
        queryset=get_user_model().objects.all(),
        expressions='username__icontains',
    )

    class Meta:
        model = Post
        widgets = {
            'date': SplitDateTimeWidget,
        }


@admin.register(Post)
class PostAdmin(CommentsModelAdminMixin, ModelAdminMixin, admin.ModelAdmin):
    form = PostAdminForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('sections', 'title', 'alias', 'preview', 'note', 'text', 'author', 'status', 'date'),
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-gallery'),
            'fields': ('gallery', ),
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-comments'),
            'fields': (),
        }),
    )
    inlines = (PostFileInline, )
    list_display = ('view', 'title', 'date', 'post_sections')
    list_display_links = ('title', )
    search_fields = ('title', )
    priveleged_fields = ('alias', )
    prepopulated_fields = {'alias': ('title', )}
    raw_id_fields = ('author', )

    suit_form_tabs = (
        ('general', _('General')),
        ('gallery', _('Gallery')),
        ('comments', _('Comments'))
    )
    suit_comments_tab = 'comments'

    def post_sections(self, obj):
        """ Колонка разделов при выводе списка """
        return ', '.join(str(item) for item in obj.sections.all())
    post_sections.short_description = _('Sections')

    def get_changeform_initial_data(self, request):
        """ Автовыбор автора """
        return {
            'author': request.user,
        }


@admin.register(PostSection)
class PostSectionAdmin(ModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'alias',)
    priveleged_fields = ['alias']
    prepopulated_fields = {'alias': ('title', )}
