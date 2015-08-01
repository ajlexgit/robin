from django.conf import settings

# Кошелек получателя
WALLET = getattr(settings, 'YANDEX_MONEY_WALLET')
if not WALLET:
    raise ValueError('Invalid YANDEX_MONEY_WALLET setting')

SECRET = getattr(settings, 'YANDEX_MONEY_SECRET')
if not SECRET:
    raise ValueError('Invalid YANDEX_MONEY_SECRET setting')

DEFAULT_DESCRIPTION = getattr(settings, 'YANDEX_MONEY_DEFAULT_DESCRIPTION')
if not DEFAULT_DESCRIPTION:
    raise ValueError('Invalid YANDEX_MONEY_DEFAULT_DESCRIPTION setting')

DEFAULT_TARGETS = getattr(settings, 'YANDEX_MONEY_DEFAULT_TARGETS')
if not DEFAULT_TARGETS:
    raise ValueError('Invalid YANDEX_MONEY_DEFAULT_TARGETS setting')


PAYMENT_URL = 'https://money.yandex.ru/quickpay/confirm.xml'