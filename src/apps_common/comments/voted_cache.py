from django.conf import settings
from django.core.cache import caches

CACHE_BACKEND = getattr(settings,  'COMMENT_USER_VOTES_CACHE_BACKEND', 'default')
cache = caches[CACHE_BACKEND]


def _get_user_voted(user):
    """ ID всех комментариев, за которые проголосовал юзер """
    from .models import CommentVote

    voted = CommentVote.objects.filter(user=user).values_list('comment__id', 'value')
    return {vote[0]: vote[1] for vote in voted}


def _cache_key(user):
    """ Ключ для хранения данных в кэше """
    return 'comments_voted:%s' % user.pk


def get_voted(user):
    """ Получение словаря комментариев, за которые проголосовал юзер """
    if not user.is_authenticated():
        return {}

    key = _cache_key(user)
    if key in cache:
        return cache.get(key)
    else:
        return update_voted_cache(user)


def update_voted_cache(user):
    """ Обновление кэша голосов юзера """
    key = _cache_key(user)
    voted = _get_user_voted(user)
    cache.set(key, voted, 3 * 24 * 3600)
    return voted

