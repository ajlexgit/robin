from django.http.response import Http404
from django.views.generic import TemplateView
from django.shortcuts import redirect
from . import providers


class CompleteView(TemplateView):
    def get(self, request):
        provider_code = request.GET.get('provider')
        if not provider_code:
            raise Http404

        provider_class = providers.PROVIDERS.get(provider_code)
        if not provider_class or not issubclass(provider_class, providers.BaseProvider):
            raise Http404

        provider = provider_class(request)
        data = provider.get_info()
        print(data)


class LoginView(TemplateView):

    def get(self, request, provider_class):
        provider = provider_class(request)
        return redirect(provider.get_authorization_url())