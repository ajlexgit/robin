from .models import PageFile

"""
    Модуль файлов на страницу.
    
    Пример:
        models.py:
            from files import PageFile
        
            class CompanyFile(PageFile):
                STORAGE_LOCATION = options.FILES_PATH
                
                company = models.ForeignKey(Company, verbose_name='Компания', related_name='files')

                def generate_filename(self, filename):
                    return '%d/%s' % (self.company.pk, filename)
        
        admin.py:
            from .models import CompanyFile
            from files.admin import PageFileInline

            class CompanyFileInline(PageFileInline):
                model = CompanyFile
"""