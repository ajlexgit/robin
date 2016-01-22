import os
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, patterns
from django.shortcuts import render, redirect
from django.core.management import call_command
from libs.download import AttachmentResponse
from .models import DummyModel


def _filesize(file):
    """ Получение размера файла """
    stat = os.stat(file)
    return stat.st_size


@admin.register(DummyModel)
class DummyAdmin(admin.ModelAdmin):
    prefix_url = 'backups'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = patterns('',
            url(r'^$', self.index, name='%s_index' % self.prefix_url),
            url(r'^create/$', self.create, name='%s_create' % self.prefix_url),
            url(r'^delete/(?P<filename>[\d_]+)/$', self.delete, name='%s_delete' % self.prefix_url),
            url(r'^download/(?P<filename>[\d_]+)/$', self.download, name='%s_download' % self.prefix_url),
        )
        return custom_urls + urls

    def index(self, request):
        """ Список бэкапов """
        zip_archives = []
        for file in sorted(os.listdir(settings.BACKUP_ROOT)):
            absfile = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))
            if os.path.isfile(absfile) and absfile.endswith('.zip'):
                zip_archives.append((
                    os.path.splitext(file)[0], _filesize(absfile)
                ))

        return render(request, 'backups/admin/index.html', {
            'prefix_url': self.prefix_url,
            'files': reversed(zip_archives),
        })

    def create(self, request):
        """ Создание бэкапа """
        call_command('zipdata')
        return redirect('admin:%s_index' % self.prefix_url)

    def delete(self, request, filename):
        """ Удаление бэкапа """
        file = '{}.zip'.format(os.path.basename(filename))
        file = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))

        if os.path.isfile(file) and file.endswith('.zip'):
            os.unlink(file)

        return redirect('admin:%s_index' % self.prefix_url)

    def download(self, request, filename):
        """ Скачаивание бэкапа """
        file = '{}.zip'.format(os.path.basename(filename))
        file = os.path.abspath(os.path.join(settings.BACKUP_ROOT, file))

        if os.path.isfile(file) and file.endswith('.zip'):
            return AttachmentResponse(request, file)

        return redirect('admin:%s_index' % self.prefix_url)
