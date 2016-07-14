from django.http.response import JsonResponse
from .forms import SubscribeForm


def subscribe(request):
    subscribe_form = SubscribeForm(request.POST)
    if subscribe_form.is_valid():
        subscribe_form.save()
        return JsonResponse({})
    else:
        return JsonResponse({
            'errors': subscribe_form.error_dict,
        }, status=400)

