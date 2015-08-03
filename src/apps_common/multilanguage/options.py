LANGUAGES = (
    {
        'code': 'en-US',
        'url': '//en.local.ru/',
    },
    {
        'code': 'ru-RU',
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
