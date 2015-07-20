from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from libs.views import TemplateExView
from . import permissions
from .models import Comment, CommentVote
from .forms import CommentForm, CommentValidationForm
from .voted_cache import update_voted_cache


class RefreshView(TemplateExView):
    """ Обновление всех комментариев """
    def get(self, request):
        content_type_id = request.GET.get('content_type') or None
        content_type = get_object_or_404(ContentType, pk=content_type_id)

        object_id = request.GET.get('object_id') or None
        try:
            obj = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            raise Http404

        context = {
            'comments': Comment.objects.get_for(obj).with_permissions(request.user),
            'form': CommentForm(auto_id=False, initial={
                'content_type': content_type_id,
                'object_id': object_id,
            }),
        }
        return JsonResponse({
            'comments': self.render_to_string(context, template='comments/comments.html'),
            'initial_form': self.render_to_string(context, template='comments/comments_form.html'),
        })


class ChangeView(TemplateExView):
    """ Редактирование комментария """
    template_name = 'comments/comment.html'

    def get(self, request):
        validation_form = CommentValidationForm(request.GET)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        try:
            permissions.check_edit(comment, request.user)
        except permissions.CommentException as e:
            return JsonResponse({
                'error': e.reason,
            })

        return JsonResponse({
            'text': comment.text
        })

    def post(self, request):
        try:
            comment_id = request.POST.get('comment') or None
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({
                'error': _('Comment not found'),
            })

        form = CommentForm(request.POST, instance=comment)
        if not form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(form.error_list),
            })

        try:
            permissions.check_edit(comment, request.user)
        except permissions.CommentException as e:
            return JsonResponse({
                'error': e.reason,
            })

        comment = form.save()
        comment.add_permissions(request.user)

        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            }),
        })


class DeleteView(TemplateExView):
    """ Удаление комментария """
    template_name = 'comments/comment.html'

    def post(self, request):
        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        try:
            permissions.check_delete(comment, request.user)
        except permissions.CommentException as e:
            return JsonResponse({
                'error': e.reason,
            })

        comment.deleted = True
        comment.deleted_by = request.user
        comment.save()
        comment.add_permissions(request.user)

        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            })
        })


class RestoreView(TemplateExView):
    """ Восстановление комментария """
    template_name = 'comments/comment.html'

    def post(self, request):
        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        try:
            permissions.check_restore(comment, request.user)
        except permissions.CommentException as e:
            return JsonResponse({
                'error': e.reason,
            })

        comment.deleted = False
        comment.deleted_by = None
        comment.save()
        comment.add_permissions(request.user)

        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            })
        })


class PostView(TemplateExView):
    """ Добавление нового комментария """
    template_name = 'comments/comment.html'

    def post(self, request):
        form = CommentForm(request.POST)
        if not form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(form.error_list),
            })

        comment = form.save(commit=False)
        comment.user = request.user

        if comment.parent:
            try:
                permissions.check_reply(comment.parent, request.user)
            except permissions.CommentException as e:
                return JsonResponse({
                    'error': e.reason,
                })
        else:
            try:
                permissions.check_add(comment, request.user)
            except permissions.CommentException as e:
                return JsonResponse({
                    'error': e.reason,
                })

        comment.save()
        comment.add_permissions(request.user)

        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            }),
        })


class VoteView(TemplateExView):
    """ Голосование за комментарий """
    template_name = 'comments/comment.html'

    def post(self, request):
        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        try:
            permissions.check_vote(comment, request.user)
        except permissions.CommentException as e:
            return JsonResponse({
                'error': e.reason,
            })

        try:
            int_vote = int(request.POST.get('is_like'))
        except (TypeError, ValueError):
            return JsonResponse({
                'error': _('Bad vote value'),
            })

        vote = CommentVote(
            comment=comment,
            user=request.user,
            value=1 if int_vote else -1,
        )
        vote.save()
        update_voted_cache(request.user)

        comment.add_permissions(request.user)

        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            })
        })
