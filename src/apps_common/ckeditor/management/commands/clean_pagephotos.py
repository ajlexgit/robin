import re
from django.apps import apps
from django.core.management import BaseCommand
from django.core.management.base import CommandError
from ...models import PagePhoto, SimplePhoto

re_pagephoto = re.compile('/page_photos/\d+/photo_(\d+)')
re_simplephotos = re.compile('/simple_photos/\d+/photo_(\d+)')


class Command(BaseCommand):
    """
        Удаление фотографий, которые не привязаны к сущностям.

        pm clean_page_photos app.modelname note text
    """
    help = 'Removes unused PagePhoto and SimplePhoto instances'

    def add_arguments(self, parser):
        parser.add_argument('model', nargs=1, help='Path to checked model class')
        parser.add_argument('--fields', nargs='*', help='list of fields in models where can be photos')

    @staticmethod
    def get_model(modelpath):
        if isinstance(modelpath, str):
            return apps.get_model(*modelpath.rsplit('.', 1))

    def handle(self, *args, **options):
        if not options['model'][0]:
            raise CommandError('model required')

        modelpath = options['model'][0]
        app, modelname = modelpath.rsplit('.', 1)
        model = apps.get_model(app, modelname)

        fields = options['fields']
        if fields:
            fields = tuple(
                model._meta.get_field(item).name
                for item in fields
            )
        else:
            fields = tuple(
                item.name
                for item in model._meta.get_fields()
                if not item.auto_created and item.get_internal_type() == 'TextField'
            )

        page_photos = PagePhoto.objects.filter(instance_id=0)
        if page_photos.exists():
            self.stdout.write('Deleting %s PagePhoto without instance' % page_photos.count())
            page_photos.delete()

        simple_photos = SimplePhoto.objects.filter(instance_id=0)
        if simple_photos.exists():
            self.stdout.write('Deleting %s SimplePhoto without instance' % simple_photos.count())
            simple_photos.delete()

        # Проверка загруженных, но отсутсвующих в тексте фотографий
        self.stdout.write('Checking fields "%s":' % '", "'.join(fields))
        for instance in model.objects.all():
            used_pagephotos = []
            for fieldname in fields:
                field_value = getattr(instance, fieldname)
                matched_ids = re_pagephoto.findall(str(field_value))
                used_pagephotos.extend(matched_ids)

            used_simplephotos = []
            for fieldname in fields:
                field_value = getattr(instance, fieldname)
                matched_ids = re_simplephotos.findall(str(field_value))
                used_simplephotos.extend(matched_ids)


            attached_unused_pagephotos = PagePhoto.objects.filter(
                app_name=app,
                model_name=modelname,
                instance_id=instance.pk,
            ).exclude(pk__in=used_pagephotos)
            if attached_unused_pagephotos:
                self.stdout.write('Deleted %s PagePhoto attached to %s (#%s)' % (
                    attached_unused_pagephotos.count(),
                    modelpath,
                    instance.pk,
                ))
                attached_unused_pagephotos.delete()


            attached_unused_simplephotos = SimplePhoto.objects.filter(
                app_name=app,
                model_name=modelname,
                instance_id=instance.pk,
            ).exclude(pk__in=used_simplephotos)
            if attached_unused_simplephotos:
                self.stdout.write('Deleted %s SimplePhoto attached to %s (#%s)' % (
                    attached_unused_simplephotos.count(),
                    modelpath,
                    instance.pk,
                ))
                attached_unused_simplephotos.delete()

        self.stdout.write('Done')
