from django.http.response import JsonResponse
from .forms import SubscribeForm
from .models import Subscriber

def subscribe(request):
    subscribe_form = SubscribeForm(request.POST)
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

        return JsonResponse({})
    else:
        return JsonResponse({
            'errors': subscribe_form.error_dict,
        }, status=400)

