#!/usr/bin/env python
import os
import sys

# -webkit-transform transition
# юзать no_fontsize/default_fontsize; border-box
# Сделать SHOW_VARIATION для StdImage + ссылку на исходник, если None
# Решить проблему получения url исходника StdImage, когда файла нет
# Seo js. Readmore.js
# Вывод ошибок формы в порядке полей
# Виджет выбора иконки из спрайта
# Проверить CommentsAdminModelMixin при добавлении сущности
# Верстка по сетке
# Google maps
# help for settings.ALIAS_IN_URL
# Gallery: zoom effect, keyboard
# help for video-bg
# Suit tabs admin everywhere

# Соц авторизация: http://django-social-auth.readthedocs.org/en/latest/installing.html
# Капча в комментах, если похоже на спам
# пагинация AJAX с предзагрузкой
# счетчики и AJAX hit

# Подумать о реализации мобильной версии
# Написание тестов
# Перевод меню

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
