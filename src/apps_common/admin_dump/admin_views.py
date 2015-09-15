import io
import os
import zipfile
from datetime import datetime
from django.conf import settings
from django.contrib import admin
from django.core.management import call_command
from django.shortcuts import render, redirect
from libs.download import AttachmentResponse

BACKUP_ROOT = os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'backup'))
if not os.path.isdir(BACKUP_ROOT):
    os.mkdir(BACKUP_ROOT, mode=0o644)


def _filesize(file):
    stat = os.stat(file)
    return stat.st_size


@admin.site.admin_view
def index(request):
    zip_archives = []
    for file in os.listdir(BACKUP_ROOT):
        absfile = os.path.abspath(os.path.join(BACKUP_ROOT, file))
        if os.path.isfile(absfile) and absfile.endswith('.zip'):
            zip_archives.append((
                os.path.splitext(file)[0], _filesize(absfile)
            ))

    return render(request, 'admin_dump/admin/index.html', {
        'files': reversed(zip_archives),
    })


@admin.site.admin_view
def create(request):
    date = datetime.now().date()
    backup_name = '{}.zip'.format(date.strftime('%d_%m_%Y'))

    with zipfile.ZipFile(os.path.join(BACKUP_ROOT, backup_name), 'w') as ziph:
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                abspath = os.path.abspath(os.path.join(root, file))
                relpath = os.path.relpath(abspath, settings.MEDIA_ROOT)
                ziph.write(abspath, os.path.join('media', relpath))

        # db dump
        buffer = io.StringIO()
        call_command('dump', stdout=buffer)
        buffer.seek(0)
        ziph.writestr('dump.json', buffer.read())
        buffer.close()

    return redirect('admin_dump:index')


@admin.site.admin_view
def delete(request, filename):
    file = '{}.zip'.format(os.path.basename(filename))
    file = os.path.abspath(os.path.join(BACKUP_ROOT, file))

    if os.path.isfile(file) and file.endswith('.zip'):
        os.unlink(file)

    return redirect('admin_dump:index')


@admin.site.admin_view
def download(request, filename):
    file = '{}.zip'.format(os.path.basename(filename))
    file = os.path.abspath(os.path.join(BACKUP_ROOT, file))

    if os.path.isfile(file) and file.endswith('.zip'):
        return AttachmentResponse(request, file)

    return redirect('admin_dump:index')