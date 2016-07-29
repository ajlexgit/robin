"""
    API для получения данных из Youtube.

    Документация:
        https://developers.google.com/youtube/v3/getting-started

    Установка:
        settings.py:
            # Ключ для Youtube API
            YOUTUBE_APIKEY = 'AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg'
"""
from . import api

__all__ = ['api']
