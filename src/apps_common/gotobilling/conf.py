from django.conf import settings


# Обязательные параметры: Merchant ID и Gateway Hash
LOGIN = settings.GOTOBILLING_MID
HASH = settings.GOTOBILLING_HASH

# Адрес, куда будет перенаправлен пользователь после успешной оплаты
SUCCESS_REDIRECT_URL = getattr(
    settings,
    'GOTOBILLING_SUCCESS_REDIRECT_URL',
    settings.LOGIN_REDIRECT_URL
)

# Адрес, куда будет перенаправлен пользователь после неудачной оплаты
FAIL_REDIRECT_URL = getattr(
    settings,
    'GOTOBILLING_FAIL_REDIRECT_URL',
    settings.LOGIN_REDIRECT_URL
)

# URL, по которому будет идти отправка форм
FORM_TARGET = 'https://secure.gotoBilling.com/gateway/transact.php'
