import os
import sys

# Виджет выбора иконки из спрайта
# проверить превью при ошибке фотки галереи
# Slider3D: span

# Gallery: восстановление из дампа
# Gallery: zoom effect, keyboard, max photos count

# Предзагрузка картинки stdimage, чтобы не сбрасывалось при обновлении
# Соц авторизаци
# Капча в комментах, если похоже на спам
# пагинация AJAX с предзагрузкой
# AJAX hit

# Написание тестов

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
