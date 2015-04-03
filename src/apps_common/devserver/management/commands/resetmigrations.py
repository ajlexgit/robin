import os
import shutil
from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        local_apps = tuple(
            path for path in apps.get_app_paths()
            if path.startswith(settings.BASE_DIR)
        )
        
        # Удаление миграций
        for path in local_apps:
            migrations_dir = os.path.join(path, 'migrations')
            if os.path.isdir(migrations_dir):
                shutil.rmtree(migrations_dir)
        
        # Создание новых миграций
        for path in local_apps:
            appname = os.path.basename(path)
            print('Create migrations for %s...' % appname)
            call_command('makemigrations', appname, verbosity=0)
        
        call_command('migrate', verbosity=0)
            