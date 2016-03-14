import os
import sys

# crop each variation
# facebook like button: https://developers.facebook.com/docs/plugins/like-button?locale=ru_RU
# text-ellipsis: https://css-tricks.com/line-clampin/
# Parallax наизнанку
# drager: блокируется вертикальный скролл Android
# подумать над плагином "конструктор галереи"

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
