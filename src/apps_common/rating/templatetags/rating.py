from django.db import models
from django.template import Library, loader
from django.db.models.functions import Coalesce
from libs.cache import cached
from ..models import RatingVote

register = Library()


@cached(time=10*60)
def get_rating():
    return {
        'count': RatingVote.objects.count(),
        'avg': RatingVote.objects.aggregate(rating=Coalesce(models.Avg('rating'), 0))['rating']
    }


@register.simple_tag(takes_context=True)
def rating(context):
    request = context.get('request')
    if not request:
        return ''

    voted = request.COOKIES.get('voted')
    try:
        voted = min(max(int(voted), 1), 5)
    except (TypeError, ValueError):
        voted = 0

    return loader.render_to_string('rating/voting.html', {
        'voted': voted,
        'rating': get_rating(),
    }, request=request)