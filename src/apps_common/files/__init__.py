"""
    Модуль файлов на страницу.

    Зависит от:
        libs.storages
        libs.download

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'files',
                ...
            )

        urls.py:
            ...
            url(r'^files/', include('files.urls', namespace='files')),

    Пример:
        # models.py:
            from django.contrib.contenttypes import generic

            class Module(models.Model):
                files = generic.GenericRelation(PageFile)

        # admin.py:
            from files.admin import PageFileInline

            class ModuleFileInline(PageFileInline):
                set_name = 'module-files'
                suit_classes = 'suit-tab suit-tab-general'
"""

from .admin import PageFileInline

__all__ = ['PageFileInline']

default_app_config = 'files.apps.Config'