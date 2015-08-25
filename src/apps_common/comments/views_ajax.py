from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from libs.views import TemplateExView
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
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': _('Authentication required'),
            })

        validation_form = CommentValidationForm(request.GET)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_edit', comment):
            return JsonResponse({
                'error': _('You don\'t have permission to edit this comment')
            })

        return JsonResponse({
            'text': comment.text
        })

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': _('Authentication required'),
            })

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

        if not request.user.has_perm('comments.can_edit', comment):
            return JsonResponse({
                'error': _('You don\'t have permission to edit this comment')
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
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': _('Authentication required'),
            })

        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_delete', comment):
            return JsonResponse({
                'error': _('You don\'t have permission to delete this comment')
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
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': _('Authentication required'),
            })

        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_restore', comment):
            return JsonResponse({
                'error': _('You don\'t have permission to restore this comment')
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
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': _('Authentication required'),
            })

        form = CommentForm(request.POST)
        if not form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(form.error_list),
            })

        comment = form.save(commit=False)
        comment.user = request.user

        if not request.user.has_perm('comments.can_post'):
            return JsonResponse({
                'error': _('You don\'t have permission to post comment'),
            })

        if comment.parent:
            if not request.user.has_perm('comments.can_reply', comment.parent):
                return JsonResponse({
                    'error': _('You can\'t reply to your own comment'),
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
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': _('Authentication required'),
            })

        validation_form = CommentValidationForm(request.POST)
        if not validation_form.is_valid():
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        comment = validation_form.cleaned_data['comment']

        if not request.user.has_perm('comments.can_vote'):
            return JsonResponse({
                'error': _('You don\'t have permission to vote for this comment'),
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
        try:
            vote.save()
        except IntegrityError:
            pass
        update_voted_cache(request.user)

        comment.add_permissions(request.user)

        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            })
        })
