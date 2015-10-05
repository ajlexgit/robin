import os
import sys

# Select2: tagging
# AttachedBlocks: ограничение на список блоков, которые можно подключать массово
# field.value_from_object вместо getattr
# Fields: from_db_value, rm SubfieldBase
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
