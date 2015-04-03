from django.contrib import admin
from django.http import JsonResponse
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
            'error': 'Комментарий не найден',
        })
        
    if not comment.can_delete(request.user):
        return JsonResponse({
            'error': 'У вас нет прав на удаление этого комментария',
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
            'error': 'Комментарий не найден',
        })
        
    if not comment.can_restore(request.user):
        return JsonResponse({
            'error': 'У вас нет прав на восстановление этого комментария',
        })
        
    comment.deleted = False
    comment.deleted_by = None
    comment.save()
    return JsonResponse({})
