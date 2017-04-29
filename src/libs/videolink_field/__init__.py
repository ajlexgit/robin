"""
    Поля для хранения ссылки на видео.

    Поддерживаются сервисы:
        1) Youtube
        2) Vimeo
        3) Rutube

    Зависит от:
        social_networks
        libs.widgets

    Пример:
        video = VideoLinkField(_('video'), providers=('youtube', ))

        > video.url
        'https://www.youtube.com/watch?v=e90UfFM2yD8'

        > video.key
        'e90UfFM2yD8'

        > video._provider
        'youtube'
"""

from .videolink import VideoLink
from .fields import VideoLinkField

__all__ = ['VideoLink', 'VideoLinkField']
