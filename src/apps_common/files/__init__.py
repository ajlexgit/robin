from .models import PageFile

"""
    Модуль файлов на страницу.

    Пример:
        models.py:
            from files import PageFile

            class ModuleFile(PageFile):
                STORAGE_LOCATION = options.FILES_PATH

                module = models.ForeignKey(Module, related_name='files')

                def generate_filename(self, filename):
                    return '%d/%s' % (self.module.pk, filename)

        admin.py:
            from .models import ModuleFile
            from files.admin import PageFileInline

            class ModuleFileInline(PageFileInline):
                model = ModuleFile
"""
