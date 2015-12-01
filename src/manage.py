import os
import sys


# aspecter + parallax
# media_inervals переделать
# новый popup проверить
# виджет выбора ссылки на сущность

# JS-отвязывание плагина в конец init
# Blocks - ссылка на создание блока
# Слайдер - блокировка при некотром условии
# AJAX-авторизация на странице регистрации
# new JS popups + show/hide return popup
# интеллектуальная прокрутка слайдов мышью, чтоб не дергалась
# Очередь анимаций JS
# Вставка Rutube в текст не работает
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке

# Comments: есть возможность написать коммент к удаленному комменту. Как быть?
# Предзагрузка картинки stdimage, чтобы не сбрасывалось при обновлении страницы

# Соц авторизаци
# пагинация AJAX с предзагрузкой
# AJAX hit

# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
