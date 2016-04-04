import os
import sys

# Приложение для переноса данных
# Paeeze модуль
# CKeditor inline
# AttachmentResponse -> class
# BlockVariants.js
# ProtectedFileField, фильтровать exe / bat и т.п.
# Admin update date
# шрифты в localStorage?
# во views добавить global context
# возможность вставки в текст колонок
# crop each variation
# Parallax наизнанку
# drager: блокируется вертикальный скролл Android
# подумать над плагином "конструктор галереи"

# Слайдер - блокировка при некотром условии
# Очередь анимаций JS
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке

# Comments: есть возможность написать коммент к удаленному комменту. Как быть?
# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
