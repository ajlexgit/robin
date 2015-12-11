import os
from django.conf import settings
from django.contrib import admin
from django.core.management import call_command
from django.shortcuts import render, redirect
from libs.download import AttachmentResponse



def _filesize(file):
    """ Получение размера файла """
    stat = os.stat(file)
    return stat.st_size


@admin.site.admin_view
def index(request):
    """ Список бэкапов """
    zip_archives = []
    for file in sorted(os.listdir(settings.BACKUP_ROOT)):
        absfile = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))
        if os.path.isfile(absfile) and absfile.endswith('.zip'):
            zip_archives.append((
                os.path.splitext(file)[0], _filesize(absfile)
            ))

    return render(request, 'admin_dump/admin/index.html', {
        'files': reversed(zip_archives),
    })


@admin.site.admin_view
def create(request):
    """ Создание бэкапа """
    call_command('zipdata')
    return redirect('admin_dump:index')


@admin.site.admin_view
def delete(request, filename):
    """ Удаление бэкапа """
    file = '{}.zip'.format(os.path.basename(filename))
    file = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))

    if os.path.isfile(file) and file.endswith('.zip'):
        os.unlink(file)

    return redirect('admin_dump:index')


@admin.site.admin_view
def download(request, filename):
    """ Скачаивание бэкапа """
    file = '{}.zip'.format(os.path.basename(filename))
    file = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))

    if os.path.isfile(file) and file.endswith('.zip'):
        return AttachmentResponse(request, file)

    return redirect('admin_dump:index')