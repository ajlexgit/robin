import os
from django.conf import settings
from django.core.management import call_command
from project import celery_app


@celery_app.task
def make_backup(max_count=None):
    """
        Создание бэкапа и удаление старых бэкапов,
        если общее кол-во файлов больше max_count
    """
    if not os.path.isdir(settings.BACKUP_ROOT):
        return

    call_command('zipdata', settings.BACKUP_ROOT)

    if max_count is None:
        return
    
    if isinstance(max_count, int) and max_count > 1:
        files = []
        for file in reversed(sorted(os.listdir(settings.BACKUP_ROOT))):
            absfile = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))
            if os.path.isfile(absfile) and absfile.endswith('.zip'):
                files.append(absfile)

        if len(files) > max_count:
            for old_file in files[max_count:]:
                os.unlink(old_file)

