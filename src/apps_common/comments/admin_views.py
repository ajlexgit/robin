from django.contrib import admin
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from .models import Comment


@require_http_methods('POST')
@admin.site.admin_view
def delete_comment(request):
    """ Удаление комментария """
    try:
        comment = Comment.objects.get(pk=request.POST.get('id'))
    except Comment.DoesNotExist:
        return JsonResponse({
            'error': _('Comment not found'),
        })

    if not request.user.has_perm('comments.can_delete', comment):
        return JsonResponse({
            'error': _('You don\'t have permission to delete this comment')
        })

    comment.deleted = True
    comment.deleted_by = request.user
    comment.save()
    return JsonResponse({})


@require_http_methods('POST')
@admin.site.admin_view
def restore_comment(request):
    """ Восстановление комментария """
    try:
        comment = Comment.objects.get(pk=request.POST.get('id'))
    except Comment.DoesNotExist:
        return JsonResponse({
            'error': _('Comment not found'),
        })

    if not request.user.has_perm('comments.can_restore', comment):
        return JsonResponse({
            'error': _('You don\'t have permission to restore this comment')
        })

    comment.deleted = False
    comment.deleted_by = None
    comment.save()
    return JsonResponse({})
