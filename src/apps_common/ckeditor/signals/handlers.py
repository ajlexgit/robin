from ..models import PagePhoto, SimplePhoto


def pre_delete(sender, **kwargs):
    """
        Удаление картинок при удалении сущности
    """
    instance = kwargs.get('instance')
    photos = PagePhoto.objects.filter(
        app_name=instance._meta.app_label,
        model_name=instance._meta.model_name,
        instance_id=instance.id)
    photos.delete()


def post_save(sender, **kwargs):
    """
        Сохраняем в картинках ID сущности, к которой они привязываются
    """
    instance = kwargs.get('instance')

    page_photos = getattr(instance, '_page_photos', ())
    for photo_id in page_photos:
        try:
            photo = PagePhoto.objects.get(id=photo_id)
        except (PagePhoto.DoesNotExist, PagePhoto.MultipleObjectsReturned):
            continue
        else:
            photo.instance_id = instance.id
            photo.save()

    simple_photos = getattr(instance, '_simple_photos', ())
    for photo_id in simple_photos:
        try:
            photo = SimplePhoto.objects.get(id=photo_id)
        except (SimplePhoto.DoesNotExist, SimplePhoto.MultipleObjectsReturned):
            continue
        else:
            photo.instance_id = instance.id
            photo.save()
