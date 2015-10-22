from django.db import IntegrityError
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from libs.views_ajax import AjaxViewMixin
from .models import Comment, CommentVote
from .forms import CommentForm, CommentValidationForm
from .voted_cache import update_voted_cache


class RefreshView(AjaxViewMixin, View):
    """ Обновление всех комментариев """
    def get(self, request):
        try:
            content_type_id = int(request.GET.get('content_type'))
            object_id = int(request.GET.get('object_id'))
        except (ValueError, TypeError):
            return self.json_response(status=400)

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
            obj = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            return self.json_response({
                'message': _('Page not found'),
            }, status=400)

        context = {
            'comments': Comment.objects.get_for(obj).with_permissions(request.user),
            'form': CommentForm(auto_id=False, initial={
                'content_type': content_type_id,
                'object_id': object_id,
            }),
        }
        return self.json_response({
            'comments': self.render_to_string('comments/comments.html', context),
            'initial_form': self.render_to_string('comments/comments_form.html', context),
        })


class ChangeView(AjaxViewMixin, View):
    """ Редактирование комментария """
    def get(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        validation_form = CommentValidationForm(request.GET)
        if not validation_form.is_valid():
            return self.json_response({
                'message': ';\n'.join(err[1][0] for err in validation_form.error_list),
            }, status=400)

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_edit', comment):
            return self.json_response({
                'message': _('You don\'t have permission to edit this comment')
            }, status=403)

        return self.json_response({
            'text': comment.text
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        try:
            comment_id = int(request.POST.get('comment'))
        except (TypeError, ValueError):
            return self.json_response({

            }, status=400)

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return self.json_response({
                'message': _('Comment not found'),
            }, status=400)

        form = CommentForm(request.POST, instance=comment)
        if not form.is_valid():
            return self.json_response({
                'message': ';\n'.join(err[1][0] for err in form.error_list),
            }, status=400)

        if not request.user.has_perm('comments.can_edit', comment):
            return self.json_response({
                'message': _('You don\'t have permission to edit this comment')
            }, status=403)

        comment = form.save()
        comment.add_permissions(request.user)

        return self.json_response({
            'html': self.render_to_string('comments/comment.html', {
                'comment': comment,
            }),
        })


class DeleteView(AjaxViewMixin, View):
    """ Удаление комментария """
    def post(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return self.json_response({
                'message': ';\n'.join(err[1][0] for err in validation_form.error_list),
            }, status=400)

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_delete', comment):
            return self.json_response({
                'message': _('You don\'t have permission to delete this comment')
            }, status=403)

        comment.deleted = True
        comment.deleted_by = request.user
        comment.save()
        comment.add_permissions(request.user)

        return self.json_response({
            'html': self.render_to_string('comments/comment.html', {
                'comment': comment,
            })
        })


class RestoreView(AjaxViewMixin, View):
    """ Восстановление комментария """
    def post(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return self.json_response({
                'message': ';\n'.join(err[1][0] for err in validation_form.error_list),
            }, status=400)

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_restore', comment):
            return self.json_response({
                'message': _('You don\'t have permission to restore this comment')
            }, status=403)

        comment.deleted = False
        comment.deleted_by = None
        comment.save()
        comment.add_permissions(request.user)

        return self.json_response({
            'html': self.render_to_string('comments/comment.html', {
                'comment': comment,
            })
        })


class PostView(AjaxViewMixin, View):
    """ Добавление нового комментария """
    def post(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        form = CommentForm(request.POST)
        if not form.is_valid():
            return self.json_response({
                'message': ';\n'.join(err[1][0] for err in form.error_list),
            }, status=400)

        comment = form.save(commit=False)
        comment.user = request.user

        if not request.user.has_perm('comments.can_post'):
            return self.json_response({
                'message': _('You don\'t have permission to post comment'),
            }, status=403)

        if comment.parent:
            if not request.user.has_perm('comments.can_reply', comment.parent):
                return self.json_response({
                    'message': _('You can\'t reply to your own comment'),
                }, status=403)

        comment.save()
        comment.add_permissions(request.user)

        return self.json_response({
            'html': self.render_to_string('comments/comment.html', {
                'comment': comment,
            }),
        })


class VoteView(AjaxViewMixin, View):
    """ Голосование за комментарий """
    def post(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return self.json_response({
                'message': ';\n'.join(err[1][0] for err in validation_form.error_list),
            }, status=400)

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_vote'):
            return self.json_response({
                'message': _('You don\'t have permission to vote for this comment'),
            }, status=403)

        try:
            int_vote = int(request.POST.get('is_like'))
        except (TypeError, ValueError):
            return self.json_response({
                'message': _('Bad vote value'),
            }, status=400)

        vote = CommentVote(
            comment=comment,
            user=request.user,
            value=1 if int_vote else -1,
        )
        try:
            vote.save()
        except IntegrityError:
            pass
        update_voted_cache(request.user)

        comment.add_permissions(request.user)

        return self.json_response({
            'html': self.render_to_string('comments/comment.html', {
                'comment': comment,
            })
        })
