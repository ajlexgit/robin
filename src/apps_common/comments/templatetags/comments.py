from django.template import Library, loader
from django.shortcuts import resolve_url
from django.contrib.contenttypes.models import ContentType
from users import options as users_options
from ..models import Comment
from ..forms import CommentForm
from ..voted_cache import get_voted

register = Library()


@register.simple_tag(takes_context=True)
def comments(context, entity, template='comments/comments_block.html'):
    request = context['request']
    request.js_storage.update(
        comment_post=resolve_url('comments:post'),
        comment_change=resolve_url('comments:change'),
        comment_delete=resolve_url('comments:delete'),
        comment_restore=resolve_url('comments:restore'),
        comment_vote=resolve_url('comments:vote'),
        comments_refresh=resolve_url('comments:refresh'),
    )

    content_type = ContentType.objects.get_for_model(type(entity))
    form = CommentForm(auto_id=False, initial={
        'content_type': content_type.pk,
        'object_id': entity.pk,
    })

    context.update({
        'content_type': content_type.pk,
        'object_id': entity.pk,
        'comments': Comment.objects.get_for(entity),
        'form': form,
        'avatar_size': users_options.AVATAR_MICRO,
    })
    return loader.render_to_string(template, context)


@register.filter
def format_rating(value):
    if value > 0:
        return '%+d' % value
    elif value < 0:
        return '–%d' % abs(value)
    else:
        return value


@register.filter
def get_vote(comment, user):
    """
    Получение голоса юзера за коммент.
    Возвращает +1, -1 или None
    """
    return get_voted(user).get(comment.id)
