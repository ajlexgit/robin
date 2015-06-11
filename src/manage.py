import os
import sys

# popups: проверить кнопку закрытия
# Избавиться от ADDITION_JS
# Предзагрузка картинки stdimage, чтобы не сбрасывалось при обновлении
# Slider3D: span

# типа ImageField но с превью и возможностью SVG
# Custom fields: юзать descriptor_class?
# Виджет выбора иконки из спрайта
# Проверить CommentsAdminModelMixin при добавлении сущности
# Gallery: zoom effect, keyboard, max photos count

# Соц авторизаци
# Капча в комментах, если похоже на спам
# пагинация AJAX с предзагрузкой
# AJAX hit

# Написание тестов

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
