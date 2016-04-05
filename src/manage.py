import os
import sys

# Admin autocomplete_filter
# Приложение для переноса данных
# Paeeze модуль
# ProtectedFileField, фильтровать exe / bat и т.п.
# возможность вставки в текст колонок
# Слайдер - блокировка при некотром условии
# crop each variation
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке

# Parallax наизнанку
# drager: блокируется вертикальный скролл Android

# Comments: есть возможность написать коммент к удаленному комменту. Как быть?
# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
