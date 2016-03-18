from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import is_valid_path
from libs.geocity import info
from .utils import get_client_ip, disable_autoredirect, noredirect_url
from . import options


class LanguageRedirectMiddleware:
    """
        Осуществляет редирект на сайт определенного языка,
        если в сессии не указано, что редирект запрещен.
    """

    @staticmethod
    def process_request(request):
        # Проверяем запрет авторедиректа через сессию
        if request.session.get(options.NOREDIRECT_SESSION_KEY, None):
            return

        # Проверяем запрет авторедиректа через Cookie
        if request.GET.get(options.NOREDIRECT_GET_PARAM):
            disable_autoredirect(request)

            # Проверяем, что на текущем сайте есть такая страница,
            # иначе, редиректим на FALLBACK_REDIRECT_URL
            urlconf = getattr(request, 'urlconf', None)
            if not is_valid_path(request.path_info, urlconf):
                return redirect(options.FALLBACK_REDIRECT_URL)

            return

        # Проверяем запрет авторедиректа для определенных User-Agent
        ua_string = request.META.get('HTTP_USER_AGENT').lower()
        for pattern in options.ROBOTS_UA:
            if pattern in ua_string:
                return

        # Получение информации о IP
        ip = get_client_ip(request)
        ip_info = info(ip, detailed=True)
        if not ip_info:
            disable_autoredirect(request)
            return

        # Определение кода языка, на который нужно редиректить
        current_code = settings.LANGUAGE_CODE
        redirect_code = current_code
        try:
            ip_iso = ip_info.get('country').get('iso')
        except AttributeError:
            pass
        else:
            for code, opts in options.LANGUAGES.items():
                iso = opts.get('iso')
                if iso and ip_iso in iso:
                    redirect_code = code
                    break

        if current_code != redirect_code:
            # отключаем редирект на текущем домене
            disable_autoredirect(request)

            language = options.LANGUAGES.get(redirect_code)
            if language:
                redirect_url = noredirect_url(language['url'], forced_path=request.path)
                return redirect(redirect_url)
