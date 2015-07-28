from django.shortcuts import redirect
from . import options
from .utils import disable_autoredirect, noredirect_url, get_referer_url


def set_lang(request, code):
    """
        Переход на сайт с выбранным языком
    """
    referer_url = get_referer_url(request)

    # язык некорректен или отсутствует
    if not code or not code in options.LANGUAGE_CODES:
        return redirect(referer_url)

    # запрещаем авторедирект на текущем домене
    disable_autoredirect(request)

    language = options.LANGUAGES_DICT.get(code)

    # запрещаем авторедирект на удаленном домене
    redirect_url = noredirect_url(language['url'], forced_path=referer_url)
    return redirect(redirect_url)
