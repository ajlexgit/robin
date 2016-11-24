from django.conf import settings

# Обязательные параметры
LOGIN_ID = settings.AUTHORIZENET_LOGIN_ID
MD5_HASH = settings.AUTHORIZENET_MD5_HASH
SEQUENCE = settings.AUTHORIZENET_SEQUENCE
TRANSACTION_KEY = settings.AUTHORIZENET_TRANSACTION_KEY


# Адрес страницы обработки результата
RESULT_URL = getattr(
    settings,
    'AUTHORIZENET_RESULT_URL',
    'authorize_net:result'
)

# Адрес, куда будет перенаправлен пользователь при отмене оплаты
CANCEL_URL = getattr(
    settings,
    'AUTHORIZENET_CANCEL_URL',
    settings.LOGIN_REDIRECT_URL
)

# Адрес ссылки возврата на сайт со страницы квитанции
RECEIPT_URL = getattr(
    settings,
    'AUTHORIZENET_RECEIPT_URL',
    None
)

# Включен ли тестовый режим
TEST_MODE = getattr(settings, 'AUTHORIZENET_TEST_MODE', False)

# URL, по которому будет идти отправка форм
FORM_TARGET = 'https://secure2.authorize.net/gateway/transact.dll'
if TEST_MODE:
    FORM_TARGET = 'https://test.authorize.net/gateway/transact.dll'

