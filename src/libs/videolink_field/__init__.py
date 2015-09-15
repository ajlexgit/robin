"""
    Поля для хранения ссылки на видео

    Установка:
        settings.py:
            # Ключ для Youtube API
            YOUTUBE_APIKEY = 'AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg'

    Пример:
        video = VideoLinkField(_('video'))
"""

from .videolink import VideoLink, BadVideoURL, NotAllowedProvider
from .fields import VideoLinkField
