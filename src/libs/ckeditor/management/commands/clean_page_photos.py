from django.core.management import BaseCommand
from ...models import PagePhoto, SimplePhoto


class Command(BaseCommand):
    """ Удаление фотографий, которые не привязаны к сущностям """
    def handle(self, *args, **options):
        page_photos = PagePhoto.objects.filter(instance_id=0)
        print('Deleting %s page photos...' % page_photos.count(), end=' ')
        page_photos.delete()
        print('Done')
        
        simple_photos = SimplePhoto.objects.filter(instance_id=0)
        print('Deleting %s simple photos...' % simple_photos.count(), end=' ')
        simple_photos.delete()
        print('Done')
        