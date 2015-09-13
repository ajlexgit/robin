import os
import sys

# Gallery: video preview SdtImage
# Gallery: make IMAGE_MODEL not required
# Проверить вставку видео в текст с Vimeo и т.п.
# Очередь анимаций JS
# Создание дампов в админке
# Предзагрузка картинки stdimage, чтобы не сбрасывалось при обновлении страницы

# multilanguage on same site

# Соц авторизаци
# пагинация AJAX с предзагрузкой
# AJAX hit

# Написание тестов

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
