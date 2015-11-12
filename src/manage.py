import os
import sys


# AJAX-авторизация на странице регистрации
# new JS popups + show/hide return popup
# Custom Radio + group
# Custom checkbox group
# SessionStoreMixin: переделать? Не работает для InlineFormset
# css background em?
# Comments: есть возможность написать коммент к удаленному комменту. Как быть?
# интеллектуальная прокрутка слайдов мышью, чтоб не дергалась
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
