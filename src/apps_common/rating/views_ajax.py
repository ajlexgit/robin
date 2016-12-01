from django.views.generic.base import View
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from libs.cookies import set_cookie
from libs.views_ajax import AjaxViewMixin
from .models import RatingVote
from .utils import get_client_ip
from . import conf


class VoteView(AjaxViewMixin, View):
    def post(self, request):
        rating = request.POST.get('rating')
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            # Если пытаешься хакнуть - голосуешь на 5 баллов :)
            rating = 5

        # проверка, что уже голосовал (по куке)
        is_voted = request.COOKIES.get('voted') is not None

        # проверка, что уже голосовал (по IP)
        client_ip = get_client_ip(request)
        is_voted = is_voted or RatingVote.objects.filter(
            ip=client_ip,
            date__gte=now() - timedelta(seconds=conf.REVOTE_PERIOD)
        )

        if is_voted:
            return self.json_response({
                'error': _('Already voted!')
            })


        # голосование
        vote = RatingVote(
            ip=client_ip,
            rating=rating,
        )
        try:
            vote.full_clean()
            vote.save()
        except ValidationError:
            return self.json_error()
        else:
            response = self.json_response()
            set_cookie(response, 'voted', rating, expires=conf.COOKIE_DAYS_EXPIRES)
            return response
