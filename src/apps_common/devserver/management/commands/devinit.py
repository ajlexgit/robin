import subprocess
from django.conf import settings
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    """
        Инициализация окружения.

        Создает БД; устанавливает iPython; добавляет алиасы py, pip, pm
    """
    def handle_noargs(self, **options):
        db = settings.DATABASES['default']
        command = 'sh {script} {dbname} {user} {password}'.format(
            script='%s/init.sh' % settings.BASE_DIR,
            dbname = db['NAME'],
            user = db['USER'],
            password = db['PASSWORD'],
        )
        subprocess.call(command, shell=True)