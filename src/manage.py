import os
import sys

# GMap marker label: http://stackoverflow.com/questions/35274487/google-maps-api-get-place-text-like-on-iframe-map
# HTML5 Manifest
# PIP -> jpegtran
# Schema.org: per page + get data from models
# Mailer antispam, proves
# Menu: выделение из вьюхи
# Admin: функция "скопировать из"
# crop each variation
# Кнопка подтверждения заказа в админке
# Редактирование продуктов магазина в админке

# Comments: есть возможность написать коммент к удаленному комменту. Как быть?
# Logging, checks, tests

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
