import os
import sys

# Ckeditor: remove format address, ...
# text_styles: $margin
# подумать над плагином аля-слайдер с двумя вертикальными фотками
# как-то упростить остановку видео при закрытии popup
# destroy внутри beforeHide вызывает call stack
# popup events
# множественные модальные окна
# Angular-like
# виджет выбора ссылки на сущность

# Blocks - ссылка на создание блока
# Слайдер - блокировка при некотром условии
# AJAX-авторизация на странице регистрации
# Очередь анимаций JS
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке

# Comments: есть возможность написать коммент к удаленному комменту. Как быть?
# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
