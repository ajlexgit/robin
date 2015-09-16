"""
    Модуль файлов на страницу.

    Зависит от:
        libs.media_storage

    Пример:
        models.py:
            from files import PageFile

            class ModuleFile(PageFile):
                STORAGE_LOCATION = options.FILES_PATH

                module = models.ForeignKey(Module, related_name='files')

                def generate_filename(self, filename):
                    return '%d/%s' % (self.module.pk, filename)

        admin.py:
            from suit.admin import SortableStackedInline
            from files.admin import PageFileInlineMixin
            from .models import ModuleFile

            class ModuleFileInline(PageFileInlineMixin, SortableStackedInline):
                model = ModuleFile
"""

from .models import PageFile