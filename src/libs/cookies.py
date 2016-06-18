from datetime import datetime, timedelta
from django.conf import settings


def set_cookie(response, key, value, expires=None):
    """
        Вспомогательная функция для установки кук.

        Параметр expires может быть None (для установки куки на время сессии);
        или числом, обозначающим кол-во дней до её истечения.
    """
    if isinstance(expires, int):
        expires = datetime.utcnow() + timedelta(days=expires)

    response.set_cookie(
        key,
        value,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None
    )
