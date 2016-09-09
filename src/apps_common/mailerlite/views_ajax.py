from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from .forms import SubscribeForm
from .models import Subscriber


class SubscribeView(AjaxViewMixin, View):
    def post(self, request):
        subscribe_form = SubscribeForm(request.POST, request.FILES)
        if subscribe_form.is_valid():
            groups = subscribe_form.cleaned_data.get('groups')
            email = subscribe_form.cleaned_data.get('email')

            try:
                subscriber = Subscriber.objects.get(email=email)
            except Subscriber.DoesNotExist:
                subscriber = Subscriber(
                    email=email,
                )
            else:
                if subscriber.status == Subscriber.STATUS_UNSUBSCRIBED:
                    subscriber.status = Subscriber.STATUS_QUEUED

            subscriber.save()
            subscriber.groups.clear()
            subscriber.groups.add(*groups)

            return self.json_response({
                'success_message': self.render_to_string('mailerlite/ajax_success.html')
            })
        else:
            return self.json_error({
                'errors': subscribe_form.error_dict_full,
            }, status=400)

