"""
    Модуль файлов на страницу.

    Зависит от:
        libs.media_storage

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'files',
                ...
            )

    Пример:
        models.py:
            from files import PageFile

            class ModuleFile(PageFile):
                STORAGE_LOCATION = 'module/files'

                module = models.ForeignKey(Module, related_name='files'

        admin.py:
            from suit.admin import SortableStackedInline
            from files.admin import PageFileInlineMixin
            from .models import ModuleFile

            class ModuleFileInline(PageFileInlineMixin, SortableStackedInline):
                model = ModuleFile
"""

from .models import PageFile

__all__ = ['PageFile']

default_app_config = 'files.apps.Config'