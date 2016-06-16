from urllib.parse import urlparse
from django.conf import settings
from django.utils.encoding import force_text
from django.shortcuts import redirect, render, resolve_url
from django.contrib.sites.shortcuts import get_current_site
from .away import is_same_domain


def away(request):
    referer = force_text(
        request.META.get('HTTP_REFERER'),
        strings_only=True,
        errors='replace'
    )
    if referer is None:
        return redirect(settings.LOGIN_REDIRECT_URL)

    referer = urlparse(referer)

    # # Убеждаемся, что в REFERER валидный урл
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
