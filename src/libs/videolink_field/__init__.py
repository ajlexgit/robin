"""
    Поля для хранения ссылки на видео.

    Зависит от:
        libs.widgets
        libs.youtube

    Пример:
        video = VideoLinkField(_('video'))
"""

from .videolink import VideoLink, BadVideoURL, NotAllowedProvider
from .fields import VideoLinkField

__all__ = ['VideoLink', 'BadVideoURL', 'NotAllowedProvider', 'VideoLinkField']