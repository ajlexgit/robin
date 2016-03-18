from django.shortcuts import redirect
from .utils import disable_autoredirect, noredirect_url, get_referer_url
from . import options


def redirect_to_language(request, code):
    """
        Переход на сайт с выбранным языком
    """
    referer_url = get_referer_url(request)

    # язык некорректен или отсутствует
    if not code or not code in options.LANGUAGES:
        return redirect(referer_url)

    # запрещаем авторедирект на текущем домене
    disable_autoredirect(request)

    # запрещаем авторедирект на удаленном домене
    language = options.LANGUAGES.get(code)
    redirect_url = noredirect_url(language['url'], forced_path=referer_url)
    return redirect(redirect_url)
