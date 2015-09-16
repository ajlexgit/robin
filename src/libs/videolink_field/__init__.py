"""
    Поля для хранения ссылки на видео.

    Зависит от:
        libs.checks
        libs.widgets
        libs.youtube_data

    Пример:
        video = VideoLinkField(_('video'))
"""

from .videolink import VideoLink, BadVideoURL, NotAllowedProvider
from .fields import VideoLinkField

__all__ = ['VideoLink', 'BadVideoURL', 'NotAllowedProvider', 'VideoLinkField']