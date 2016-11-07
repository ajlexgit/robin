import os
import sys

# Блок в шаблоне, который может быть AJAX или нет - по флагу
# CKEditor internal link
# $.fn.scrolltextarea + autosize
# Mailerlite: clear subscribers from remote + limit reached + select groups on import
# Shop cart example + discounts
# Share: выводить картинку и дать возможность изменить
# Mobile tables
# Images: alt, title, file name
# Schema.org: per page + get data from models
# Admin: функция "скопировать из"
# crop each variation
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке
# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
