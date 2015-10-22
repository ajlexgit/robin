import os
import sys

# Uploader: use uploader.js
# Google Maps: bounds + upgrade JS, $.GoogleMapsReady(handler), str longitude after get_or_create,
#              marker options
# создать JS, сохраняющий CSS и восстанавливающий их
# Comments: есть возможность написать коммент к удаленному комменту. Как быть?
# интеллектуальная проркутка слайдов мышью, чтоб не дергалась
# Очередь анимаций JS
# Предзагрузка картинки stdimage, чтобы не сбрасывалось при обновлении страницы
# Вставка Rutube в текст не работает

# Соц авторизаци
# пагинация AJAX с предзагрузкой
# AJAX hit

# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
