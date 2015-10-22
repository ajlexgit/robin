from django.contrib import admin
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from libs.views_ajax import AjaxViewMixin
from .models import Comment


class DeleteView(AjaxViewMixin, View):
    """ Удаление комментария """
    def get_handler(self, request):
        handler = super().get_handler(request)
        if handler:
            handler = admin.site.admin_view(handler)
        return handler

    def post(self, request):
        try:
            comment = Comment.objects.get(pk=request.POST.get('id'))
        except Comment.DoesNotExist:
            return self.json_response({
                'error': _('Comment not found'),
            })


        if not request.user.has_perm('comments.can_delete', comment):
            return self.json_response({
                'error': _('You don\'t have permission to delete this comment')
            })

        comment.deleted = True
        comment.deleted_by = request.user
        comment.save()
        return self.json_response()


class RestoreView(AjaxViewMixin, View):
    """ Восстановление комментария """
    def get_handler(self, request):
        handler = super().get_handler(request)
        if handler:
            handler = admin.site.admin_view(handler)
        return handler

    def post(self, request):
        try:
            comment = Comment.objects.get(pk=request.POST.get('id'))
        except Comment.DoesNotExist:
            return self.json_response({
                'error': _('Comment not found'),
            })


        if not request.user.has_perm('comments.can_restore', comment):
            return self.json_response({
                'error': _('You don\'t have permission to restore this comment')
            })

        comment.deleted = False
        comment.deleted_by = None
        comment.save()
        return self.json_response()
