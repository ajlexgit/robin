import os
import sys

# text-ellipsis: https://css-tricks.com/line-clampin/
# Susy
# Angular-like
# Parallax наизнанку
# виджет выбора ссылки на сущность
# подумать над плагином "конструктор плагина"

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
