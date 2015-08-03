import os
from django.db import models
from django.apps import apps
from django.conf import settings
from django.core import management
from libs.variation_field import VariationImageFieldFile

"""
    Позволяет получить список файлов из папки MEDIA_ROOT, не упомянутых в БД, и/или удалить их.
    Работает со стандартными полями FileField / ImageField и с полями VariationImageField и
    их наследниками (StdImageField, GalleryImageField)
"""


class Command(management.BaseCommand):

    def handle(self, *args, **options):
        media_files = []

        # Получаем список файлов в папке MEDIA
        for path, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                media_files.append(os.path.join(path, file))

        # Удаляем ссылки на файлы, которые упомянуты в БД
        for model in apps.get_models():
            file_fields = []
            for field in model._meta.concrete_fields:
                if isinstance(field, models.FileField):
                    file_fields.append(field.name)

            if file_fields:
                objects = model.objects.all().only(*file_fields)
                for object in objects:
                    for field in file_fields:
                        filefield = getattr(object, field, None)
                        if filefield.name and filefield.storage.exists(filefield.name):

                            # Стандартное поле файла
                            path = filefield.storage.path(filefield.name)
                            if path in media_files:
                                media_files.remove(path)

                            # Вариации
                            if isinstance(filefield, VariationImageFieldFile):
                                for path in filefield.variation_files:
                                    final_path = filefield.storage.path(path)
                                    if final_path in media_files:
                                        media_files.remove(final_path)

        if not media_files:
            print('Unused files not found...')
            return

        answer = input('Founded %s unused files. Do you want to save list (y/n)? ' % len(media_files))
        answer = answer.lower()
        if answer == 'y':
            answer = input('Type output filename (like "mylist.log") or leave it empty for dump to console.\n> ')

            if answer:
                path = os.path.normpath(os.path.join('/tmp/', os.path.basename(answer)))
                with open(path, 'w+') as output:
                    for item in media_files:
                        output.write(item + '\n')

                print('Dump saved in file %r' % path)
            else:
                print('-' * 20)
                for item in media_files:
                    print(item)
                print('-' * 20)

        answer = input('Do you want to DELETE all founded unused files (y/n)? ')
        answer = answer.lower()
        if answer == 'y':
            for item in media_files:
                if os.path.exists(item):
                    os.remove(item)

        print('Done')
