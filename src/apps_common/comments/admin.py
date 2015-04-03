from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from suit.widgets import AutosizedTextarea
from libs.widgets import SplitDateTimeWidget
from project.admin import ModelAdminMixin
from .models import Comment


class CommentsModelAdminMixin:
    """
        Модель админки, добавляющая к форме блок комментариев на сущность
    """
    suit_comments_position = 'top'
    suit_comments_tab = None
    
    class Media:
        js = (
            'comments/admin/js/comments.js',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_includes = getattr(self, 'suit_form_includes', ())
        self.suit_form_includes = default_includes + (
            ('comments/admin/admin_include.html', self.suit_comments_position, self.suit_comments_tab),
        )
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        entity = None
        comments = ()
        if object_id:
            try:
                entity = self.model.objects.get(pk=object_id)
            except self.model.DoesNotExist:
                pass
            content_type = ContentType.objects.get_for_model(self.model)
            comments = Comment.objects.filter(
                content_type = content_type.pk,
                object_id = object_id,
            ).select_related('user__pk', 'user__username', 'user__avatar')
        
        
        extra_context = extra_context or {}
        extra_context.update({
            'comments': comments,
            'comment_level_indent': 20,
            'entity': entity,
        })
        return super().change_view(request, object_id, form_url, extra_context)
    
    
class CommentAdminForm(forms.ModelForm):
    class Meta:
        models = Comment
        exclude = ('content_type', 'object_id', 'parent', )
        widgets = {
            'text': AutosizedTextarea(attrs={'rows': 3, 'class': 'span10'}),
            'created': SplitDateTimeWidget(),
        }


@admin.register(Comment)
class CommentAdmin(ModelAdminMixin, admin.ModelAdmin):
    model = Comment
    form = CommentAdminForm
    list_display = ('short_text', 'user', 'deleted', 'created')
    list_display_links = ('short_text', )
    readonly_fields = ('user', 'rating', 'created', 'deleted', 'deleted_by')
    
    class Media:
        js = (
            'comments/admin/js/comments.js',
        )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        return ()
        