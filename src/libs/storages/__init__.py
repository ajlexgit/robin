"""
    Хранилища файлов.

    1) Разделение статики по доменам:
        MEDIA_URLS = (
            '//media1.local.com',
            '//media2.local.com',
        )
"""
from .media_storage import MediaStorage

__all__ = ['MediaStorage']