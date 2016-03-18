LANGUAGES = {
    'en': {
        'url': '//local.com/',
    },
    'ru': {
        'url': '//local.ru/',
        'iso': ('RU', 'UA'),
    }
}


# если авторедирект на текущий сайт приводит на страницу,
# которой нет - редиректим на страницу FALLBACK_REDIRECT_URL
FALLBACK_REDIRECT_URL = 'index'

# имя ключа сессии, хранящего флаг того,
# что редиректить автоматически не нужно
NOREDIRECT_SESSION_KEY = 'language_setted'

# Имя GET-параметра, запрещающего авторедирект
NOREDIRECT_GET_PARAM = 'noredirect'

# Путь редиректа по умолчанию.
DEFAULT_REDIRECT_URL = 'index'

# Строки в User-Agent, которые не должны редиректиться
ROBOTS_UA = tuple(map(str.lower, (
    'Googlebot',
    'Mail.RU_Bot',
    'YandexBot',
    'YandexImage',
    'YandexMetrika',
    'Applebot',
    'facebookexternalhit',
    'DuckDuckBot',
    'SkypeUriPreview',
    'Pinterest',
    'Twitterbot',
    'Slackbot',
    'vkShare',
    'Yahoo',
    'W3C_Validator',
)))
