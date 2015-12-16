import os
import sys

# Angular-like
# Подписи к каждому слайду в тексте
# виджет выбора ссылки на сущность

# Blocks - ссылка на создание блока
# Слайдер - блокировка при некотром условии
# AJAX-авторизация на странице регистрации
# Очередь анимаций JS
# Вставка Rutube в текст не работает
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке

# Comments: есть возможность написать коммент к удаленному комменту. Как быть?

# Соц авторизаци
# пагинация AJAX с предзагрузкой
# AJAX hit

# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
