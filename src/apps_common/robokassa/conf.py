from django.conf import settings


# Обязательные параметры - реквизиты магазина
LOGIN = settings.ROBOKASSA_LOGIN
PASSWORD1 = settings.ROBOKASSA_PASSWORD1

# Его можно не указывать, если django-robokassa-payments
# используется только для вывода формы платежа.
# Если django-robokassa-payments используется для приема платежей,
# то этот параметр обязательный.
PASSWORD2 = getattr(settings, 'ROBOKASSA_PASSWORD2', None)

# Используется ли метод POST при приеме результатов от ROBOKASSA. По умолчанию - True.
# Считается, что для Result URL, Success URL и Fail URL выбран один и тот же метод
USE_POST = getattr(settings, 'ROBOKASSA_USE_POST', True)

# Использовать ли строгую проверку (требовать предварительного уведомления на ResultURL).
# По умолчанию - True
STRICT_CHECK = getattr(settings, 'ROBOKASSA_STRICT_CHECK', True)

# Адрес или имя view, куда будет перенаправлен пользователь
# При переходе на SuccessURL
SUCCESS_REDIRECT_URL = getattr(
    settings,
    'ROBOKASSA_SUCCESS_REDIRECT_URL',
    settings.LOGIN_REDIRECT_URL
)

# Адрес или имя view, куда будет перенаправлен пользователь
# При переходе на FailURL
FAIL_REDIRECT_URL = getattr(
    settings,
    'ROBOKASSA_FAIL_REDIRECT_URL',
    settings.LOGIN_REDIRECT_URL
)

# Включен ли тестовый режим. По умолчанию False (т.е. включен боевой режим)
TEST_MODE = getattr(settings, 'ROBOKASSA_TEST_MODE', False)

# URL, по которому будет идти отправка форм
FORM_TARGET = 'https://merchant.roboxchange.com/Index.aspx'

# Список (list) названий дополнительных параметров, которые будут передаваться вместе с запросами.
# Имена параметров ДОЛЖНЫ начинаться с "shp_"
EXTRA_PARAMS = sorted(getattr(settings, 'ROBOKASSA_EXTRA_PARAMS', []))
