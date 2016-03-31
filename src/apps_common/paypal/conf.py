from django.conf import settings


# Обязательные параметры: email аккаунта получателя
EMAIL = settings.PAYPAL_EMAIL

CURRENCY = getattr(
    settings,
    'PAYPAL_CURRENCY',
    'USD'
)

# Включен ли тестовый режим
TEST_MODE = getattr(settings, 'PAYPAL_TEST_MODE', False)

# URL, по которому будет идти отправка форм
FORM_TARGET = 'https://www.paypal.com/cgi-bin/webscr'
if TEST_MODE:
    FORM_TARGET = 'https://www.sandbox.paypal.com/cgi-bin/webscr'

# Адрес страницы обработки результата
RESULT_URL = getattr(
    settings,
    'PAYPAL_RESULT_URL',
    'paypal:result'
)

# Адрес, куда будет перенаправлен пользователь после успешной оплаты
SUCCESS_URL = getattr(
    settings,
    'PAYPAL_SUCCESS_URL',
    settings.LOGIN_REDIRECT_URL
)

# Адрес, куда будет перенаправлен пользователь после неудачной оплаты
CANCEL_URL = getattr(
    settings,
    'PAYPAL_CANCEL_URL',
    settings.LOGIN_REDIRECT_URL
)
