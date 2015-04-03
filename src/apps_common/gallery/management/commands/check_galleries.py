from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from ...models import GalleryBase


class Command(BaseCommand):
    """ Проверка всех галерей на объекты-зомби """
    def handle(self, *args, **options):
        gallery_models = (
            model 
            for model in apps.get_models()
                if issubclass(model, GalleryBase)
        )
        
        for gallery_model in gallery_models:
            related_names = [
                rel.get_accessor_name() 
                for rel in gallery_model._meta.get_all_related_objects()
            ]
            
            all_galleries = gallery_model.objects.all()
            for gallery in all_galleries:
                # Проверяем галереи-зомби
                for related_name in related_names:
                    try:
                        getattr(gallery, related_name)
                    except ObjectDoesNotExist:
                        print('{0.__class__.__name__} #{0.pk}: empty relation {1!r}'.format(gallery, related_name))
                
                # Проверяем пустые галереи
                if not gallery.items.count():
                    print('{0.__class__.__name__} #{0.pk}: no items'.format(gallery))
                else:
                    # Проверяем битые картинки
                    for image_item in gallery.image_items:
                        if not image_item.image:
                            print('{0.__class__.__name__} #{0.pk}, {1.__class__.__name__} #{1.pk}: have empty image item #{1.pk}'.format(gallery, image_item))
                        elif not image_item.image.exists():
                            print('{0.__class__.__name__} #{0.pk}, {1.__class__.__name__} #{1.pk}: file {1.image.name!r} not found'.format(gallery, image_item))
                