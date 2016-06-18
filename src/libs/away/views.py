from urllib.parse import urlparse
from django.conf import settings
from django.shortcuts import redirect, render, resolve_url
from django.contrib.sites.shortcuts import get_current_site
from .away import is_same_domain


def away(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return redirect(settings.LOGIN_REDIRECT_URL)

    # Убеждаемся, что в REFERER валидный урл
    referer = urlparse(referer)
    if '' in (referer.scheme, referer.netloc):
        return redirect(settings.LOGIN_REDIRECT_URL)

    # Проверяем, что переход с нашего сайта
    site = get_current_site(request)
    if not is_same_domain(referer.netloc, site.domain):
        return redirect(settings.LOGIN_REDIRECT_URL)

    url = request.GET.get('url') or resolve_url('index')
    return render(request, 'away/away.html', {
        'url': url
    })
