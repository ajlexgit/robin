#!/usr/bin/env python
import os
import sys

# Написание тестов
# Верстка по сетке
# Перевод меню
# Google maps
# help for settings.ALIAS_IN_URL
# Gallery: zoom effect, keyboard
# help for video-bg

# Соц авторизация: http://django-social-auth.readthedocs.org/en/latest/installing.html
# Капча в комментах, если похоже на спам
# пагинация AJAX с предзагрузкой
# счетчики и AJAX hit

# Подумать о реализации мобильной версии

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
