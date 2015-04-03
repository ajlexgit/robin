from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from libs.string_view import RenderToStringMixin
from . import options
from .models import Comment, CommentVote
from .forms import CommentForm, CommentValidationForm
from .voted_cache import update_voted_cache


class RefreshView(RenderToStringMixin, View):
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
            'comments': Comment.objects.get_for(obj),
            'form': CommentForm(auto_id=False, initial={
                'content_type': content_type_id,
                'object_id': object_id,
            }),
        }
        return JsonResponse({
            'comments': self.render_to_string(context, template='comments/comments.html'),
            'initial_form': self.render_to_string(context, template='comments/comments_form.html'),
        })


class ChangeView(RenderToStringMixin, TemplateView):
    """ Редактирование комментария """
    template_name = 'comments/comment.html'

    def get(self, request):
        validation_form = CommentValidationForm(request.GET)
        if validation_form.is_valid():
            comment = validation_form.cleaned_data['comment']
        else:
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        if not comment.can_edit(request.user):
            return JsonResponse({
                'error': 'У вас нет прав на редактирование этого комментария',
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
                'error': 'Комментарий не найден',
            })

        if not comment.can_edit(request.user):
            return JsonResponse({
                'error': 'У вас нет прав на редактирование этого комментария',
            })

        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return JsonResponse({
                'html': self.render_to_string({
                    'comment': comment,
                }),
            })
        else:
            return JsonResponse({
                'error': ';\n'.join(form.error_list),
            })


class DeleteView(RenderToStringMixin, TemplateView):
    """ Удаление комментария """
    template_name = 'comments/comment.html'

    def post(self, request):
        validation_form = CommentValidationForm(request.POST)
        if validation_form.is_valid():
            comment = validation_form.cleaned_data['comment']
        else:
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        if not comment.can_delete(request.user):
            return JsonResponse({
                'error': 'У вас нет прав на удаление этого комментария',
            })

        comment.deleted = True
        comment.deleted_by = request.user
        comment.save()
        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            })
        })


class RestoreView(RenderToStringMixin, TemplateView):
    """ Восстановление комментария """
    template_name = 'comments/comment.html'

    def post(self, request):
        validation_form = CommentValidationForm(request.POST)
        if validation_form.is_valid():
            comment = validation_form.cleaned_data['comment']
        else:
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        if not comment.can_restore(request.user):
            return JsonResponse({
                'error': 'У вас нет прав на восстановление этого комментария',
            })

        comment.deleted = False
        comment.deleted_by = None
        comment.save()
        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            })
        })


class PostView(RenderToStringMixin, TemplateView):
    """ Добавление нового комментария """
    template_name = 'comments/comment.html'

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': 'Для отправки комментария необходимо авторизоваться',
            })

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if comment.parent and not comment.parent.can_reply(request.user):
                return JsonResponse({
                    'error': 'Вы не можете отвечать на свой комментарий',
                })
            
            comment.user = request.user
            comment.save()

            return JsonResponse({
                'html': self.render_to_string({
                    'comment': comment,
                }),
            })
        else:
            return JsonResponse({
                'error': ';\n'.join(form.error_list),
            })


class VoteView(RenderToStringMixin, TemplateView):
    """ Голосование за комментарий """
    template_name = 'comments/comment.html'
    
    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({
                'error': 'Для оценки комментариев необходимо авторизоваться',
            })
        
        validation_form = CommentValidationForm(request.POST)
        if validation_form.is_valid():
            comment = validation_form.cleaned_data['comment']
        else:
            return JsonResponse({
                'error': ';\n'.join(validation_form.error_list),
            })

        if not options.ALLOW_SELF_VOTE and comment.user == request.user:
            return JsonResponse({
                'error': 'Вы не можете голосовать за свой комментарий',
            })
        
        try:
            is_like = int(request.POST.get('is_like'))
        except (TypeError, ValueError):
            return JsonResponse({
                'error': 'Оценка некорректна',
            })
            
        try:
            CommentVote(
                comment=comment,
                user=request.user,
                value=1 if is_like else -1,
            ).save()
        except IntegrityError:
            return JsonResponse({
                'error': 'Вы уже проголосовали за этот комментарий',
            })
        
        # Обновление кэша голосов юзера
        update_voted_cache(request.user)
        
        return JsonResponse({
            'html': self.render_to_string({
                'comment': comment,
            })
        })
