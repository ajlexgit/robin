import re
from django.apps import apps
from optparse import make_option
from django.core.management import BaseCommand
from ...models import PagePhoto, SimplePhoto

re_pagephoto = re.compile('/page_photos/\d+/photo_(\d+)')
re_simplephotos = re.compile('/simple_photos/\d+/photo_(\d+)')


class Command(BaseCommand):
    """
        Удаление фотографий, которые не привязаны к сущностям.

        Для дополнительной проверки на привязанные, но не используемые фотки,
        необходимо указать модель и поля этой модели, которые могут содержать ссылки на фотки:

        pm clean_page_photos note text --model=app.modelname
    """

    option_list = BaseCommand.option_list + (
        make_option('--model', action='store', dest='model', type='string',
            help='Model for check unused photos'),
    )

    def handle(self, *args, **options):
        page_photos = PagePhoto.objects.filter(instance_id=0)
        print('Deleting %s page photos...' % page_photos.count(), end=' ')
        page_photos.delete()
        print('Done')

        simple_photos = SimplePhoto.objects.filter(instance_id=0)
        print('Deleting %s simple photos...' % simple_photos.count(), end=' ')
        simple_photos.delete()
        print('Done')

        # Unused photos
        modelpath = options.get('model')
        fields = args
        if not modelpath or not fields:
            return

        # Check model and fields
        app, modelname = modelpath.rsplit('.', 1)
        model = apps.get_model(app, modelname)
        for field in fields:
            model._meta.get_field(field)

        for instance in model.objects.all():
            used_pagephotos = []
            for field in fields:
                field_value = getattr(instance, field)
                matched_ids = re_pagephoto.findall(str(field_value))
                used_pagephotos.extend(matched_ids)

            used_simplephotos = []
            for field in fields:
                field_value = getattr(instance, field)
                matched_ids = re_simplephotos.findall(str(field_value))
                used_simplephotos.extend(matched_ids)


            attached_unused_pagephotos = PagePhoto.objects.filter(
                app_name=app,
                model_name=modelname,
                instance_id=instance.pk,
            ).exclude(pk__in=used_pagephotos)
            if attached_unused_pagephotos:
                print('Deleted %s page photos attached to %s (#%s)' % (
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
                print('Deleted %s simple photos attached to %s (#%s)' % (
                    attached_unused_simplephotos.count(),
                    modelpath,
                    instance.pk,
                ))
                attached_unused_simplephotos.delete()
