from django.conf import settings
from django.shortcuts import redirect
from libs.geocity import info
from . import options
from .utils import get_client_ip, disable_autoredirect, noredirect_url


class LanguageRedirectMiddleware:
    """
        Осуществляет редирект на сайт определенного языка,
        если в сессии не указано, что редирект запрещен.
    """

    @staticmethod
    def process_request(request):
        # Проверяем принудительный запрет авторедиректа
        if request.GET.get(options.NOREDIRECT_GET_PARAM):
            disable_autoredirect(request)
            return

        noredirect_session = request.session.get(options.NOREDIRECT_SESSION_KEY, None)
        if not noredirect_session:
            # авторедирект разрешен
            ip = get_client_ip(request)
            ip_info = info(ip, detailed=True)
            if not ip_info:
                disable_autoredirect(request)
                return

            current_code = settings.LANGUAGE_CODE
            try:
                ip_iso = ip_info.get('country').get('iso')
            except AttributeError:
                pass
            else:
                for lang in options.LANGUAGES:
                    iso = lang.get('iso')
                    if iso and ip_iso in iso:
                        current_code = 'ru'
                        break

            language = options.LANGUAGES_DICT.get(current_code)
            if language:
                # язык сессии не совпадает с языком сайта - редиректим
                if language['code'] != settings.LANGUAGE_CODE:
                    redirect_url = noredirect_url(language['url'], forced_path=request.path)
                    return redirect(redirect_url)
