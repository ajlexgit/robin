import os
import re
from django.apps import apps
from django.core.management import BaseCommand
from libs.stdimage.fields import StdImageField


class Command(BaseCommand):
    help = 'Replace undescore in StdImage'

    def rename_image(self, in_file):
        dirname, basename = os.path.split(in_file)
        filename, ext = os.path.splitext(basename)
        filename = re.sub(r'_(\d+)', '-\\1', filename)
        basename = ''.join((filename, ext))
        return os.path.join(dirname, basename)

    def handle(self, *args, **options):
        for model in apps.get_models():
            if not model._meta.managed:
                continue

            # поля, хранящие файлы
            image_fields = [
                field.name
                for field in model._meta.get_fields()
                if isinstance(field, StdImageField)
                ]
            if not image_fields:
                continue

            # фильтрация файлов
            instances = model.objects.all().only(*image_fields)
            for instance in instances:
                updates = {}

                for field in image_fields:
                    filefield = getattr(instance, field)
                    if not filefield.name or not filefield.storage.exists(filefield.name):
                        continue

                    os.rename(filefield.path, self.rename_image(filefield.path))
                    for path in filefield.variation_files:
                        filepath = filefield.storage.path(path)
                        os.rename(filepath, self.rename_image(filepath))

                    updates[field] = self.rename_image(filefield.name)

                if updates:
                    print(model._meta.verbose_name, updates)
                    model.objects.filter(pk=instance.pk).update(**updates)
