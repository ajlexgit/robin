from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from libs.views_ajax import AjaxAdminViewMixin
from .models import Comment


class DeleteView(AjaxAdminViewMixin, View):
    """ Удаление комментария """
    def post(self, request):
        try:
            comment = Comment.objects.get(pk=request.POST.get('id'))
        except Comment.DoesNotExist:
            return self.json_error({
                'message': _('Comment not found'),
            })


        if not request.user.has_perm('comments.can_delete', comment):
            return self.json_error({
                'message': _('You don\'t have permission to delete this comment')
            }, status=403)

        comment.deleted = True
        comment.deleted_by = request.user
        comment.save()
        return self.json_response()


class RestoreView(AjaxAdminViewMixin, View):
    """ Восстановление комментария """
    def post(self, request):
        try:
            comment = Comment.objects.get(pk=request.POST.get('id'))
        except Comment.DoesNotExist:
            return self.json_error({
                'message': _('Comment not found'),
            })


        if not request.user.has_perm('comments.can_restore', comment):
            return self.json_error({
                'message': _('You don\'t have permission to restore this comment')
            }, status=403)

        comment.deleted = False
        comment.deleted_by = None
        comment.save()
        return self.json_response()
