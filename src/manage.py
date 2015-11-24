import os
import sys


# grid flex; rm gc-alone
# default_font -> font_default
# default_fontsize -> fontsize_default
# JSON.parse в try catch
# AJAX-авторизация на странице регистрации
# new JS popups + show/hide return popup
# css background em?
# интеллектуальная прокрутка слайдов мышью, чтоб не дергалась
# Очередь анимаций JS
# Вставка Rutube в текст не работает
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке

# SessionStoreMixin: переделать? Не работает для InlineFormset
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
