import os
from django.db import models
from django.apps import apps
from django.conf import settings
from django.core.management.base import NoArgsCommand
from libs.variation_field import VariationImageFieldFile


class Command(NoArgsCommand):
    """
        Позволяет получить список файлов из папки MEDIA_ROOT, не упомянутых в БД, и/или удалить их.
        Работает со стандартными полями FileField / ImageField и с полями VariationImageField и
        их наследниками (StdImageField, GalleryImageField)
    """
    help = 'Find unused media files'

    @staticmethod
    def get_all_media_files():
        """ Получаем список файлов в папке MEDIA """
        result = []
        for path, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                result.append(os.path.join(path, file))
        return result

    def filter_db_files_list(self, files_list):
        """ Удаляем ссылки на файлы, которые упомянуты в БД """
        for model in apps.get_models():
            if not model._meta.managed:
                continue

        for model in apps.get_models():
            # поля, хранящие файлы
            file_fields = [
                field.name
                for field in model._meta.get_fields()
                if isinstance(field, models.FileField)
            ]
            if not file_fields:
                continue

            # фильтрация файлов
            instances = model.objects.all().only(*file_fields)
            for instance in instances:
                for field in file_fields:
                    filefield = getattr(instance, field)
                    if not filefield.name or not filefield.storage.exists(filefield.name):
                        continue

                    pathes = self._get_filefield_files(filefield)
                    if isinstance(filefield, VariationImageFieldFile):
                        pathes.extend(self._get_filefield_variations_files(filefield))

                    for path in pathes:
                        if path in files_list:
                            files_list.remove(path)


    def _get_filefield_files(self, filefield):
        """ Путь к файлам FileField / ImageField """
        return [filefield.storage.path(filefield.name)]

    def _get_filefield_variations_files(self, filefield):
        """ Путь к файлам VariationImageFieldFile """
        return [
            filefield.storage.path(path)
            for path in filefield.variation_files
        ]

    def add_arguments(self, parser):
        parser.add_argument('--delete',
            action='store_true',
            dest='delete',
            help='Delete founded unused files'
        )

    def handle_noargs(self, **options):
        media_files = self.get_all_media_files()
        self.filter_db_files_list(media_files)
        if not media_files:
            return

        if options['delete']:
            for filepath in media_files:
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            for filepath in media_files:
                self.stdout.write(filepath)
