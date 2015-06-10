import os
import shutil
from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        local_apps = {
            app.__name__.rsplit('.', 1)[0] : os.path.dirname(app.__file__) for app in apps.get_apps()
            if app.__file__.startswith(settings.BASE_DIR)
        }

        if args:
            ok = True
            result_apps = {}
            for arg in args:
                if arg in local_apps:
                    result_apps[arg] = local_apps[arg]
                else:
                    ok = False
                    print('"%s" app not found' % arg)

            if not ok:
                return
        else:
            result_apps = local_apps

        # Удаление миграций
        for name, path in result_apps.items():
            migrations_dir = os.path.join(path, 'migrations')
            if os.path.isdir(migrations_dir):
                shutil.rmtree(migrations_dir)

        # Создание новых миграций
        for name, path in result_apps.items():
            print('Create migrations for %s...' % name)
            call_command('makemigrations', name.rsplit('.', 1)[-1], verbosity=0)

        call_command('migrate', verbosity=0)
