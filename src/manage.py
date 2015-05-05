#!/usr/bin/env python
import os
import sys

# типа ImageField но с превью и возможностью SVG
# Custom fields: юзать descriptor_class?
# Сделать SHOW_VARIATION для StdImage + ссылку на исходник, если None
# Решить проблему получения url исходника StdImage, когда файла нет
# Виджет выбора иконки из спрайта
# Проверить CommentsAdminModelMixin при добавлении сущности
# Google maps
# help for settings.ALIAS_IN_URL
# Gallery: zoom effect, keyboard

# Соц авторизация: http://django-social-auth.readthedocs.org/en/latest/installing.html
# Капча в комментах, если похоже на спам
# пагинация AJAX с предзагрузкой
# счетчики и AJAX hit

# Написание тестов

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
