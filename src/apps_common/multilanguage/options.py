import re

LANGUAGES = (
    {
        'code': 'en-US',
        'short_code': 'en',
        'url': '//en.local.ru/',
    },
    {
        'code': 'ru-RU',
        'short_code': 'ru',
        'url': '//ru.local.ru/',
        'iso': ('RU', 'UA'),
    },
)
LANGUAGES_DICT = {
    item['code']: item
    for item in LANGUAGES
}
LANGUAGE_CODES = tuple(item['code'] for item in LANGUAGES)


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
