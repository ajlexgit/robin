import os
import sys

# TextField max_length error
# GIF palette, optimize photo size
# DC meta
# попробовать другой storage
# Last-modified прицепить к sitemap
# Gallery admin: custom form
# $.widget
# Импорты для Django 1.9
# Слайдер в тексте - описания к каждой картинке
# Подумать над возможностью реализации Grid через Flexbox.
# Paginator: переделать номера страниц, чтобы их кол-во было более постоянно
# Попытаться избавиться от select_subclasses

# Shop cart example + discounts
# Gallery popup: JS templates
# $.fn.scrolltextarea + autosize
# Mailerlite: clear subscribers from remote + limit reached + select groups on import
# Share: выводить картинку и дать возможность изменить
# Mobile tables
# Images: alt, title, file name
# Schema.org: per page + get data from models
# Admin: функция "скопировать из"
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке
# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
