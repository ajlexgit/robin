from ..models import PagePhoto, PageFile, SimplePhoto


def delete_photos(sender, **kwargs):
    """
        Удаление картинок при удалении сущности
    """
    instance = kwargs.get('instance')
    pagephotos = PagePhoto.objects.filter(
        app_name=instance._meta.app_label,
        model_name=instance._meta.model_name,
        instance_id=instance.id)
    pagephotos.delete()

    pagefiles = PageFile.objects.filter(
        app_name=instance._meta.app_label,
        model_name=instance._meta.model_name,
        instance_id=instance.id)
    pagefiles.delete()

    simplephotos = SimplePhoto.objects.filter(
        app_name=instance._meta.app_label,
        model_name=instance._meta.model_name,
        instance_id=instance.id)
    simplephotos.delete()


def save_photos(sender, **kwargs):
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

    page_files = getattr(instance, '_page_files', ())
    for file_id in page_files:
        try:
            file = PageFile.objects.get(id=file_id)
        except (PageFile.DoesNotExist, PageFile.MultipleObjectsReturned):
            continue
        else:
            file.instance_id = instance.id
            file.save()

    simple_photos = getattr(instance, '_simple_photos', ())
    for photo_id in simple_photos:
        try:
            photo = SimplePhoto.objects.get(id=photo_id)
        except (SimplePhoto.DoesNotExist, SimplePhoto.MultipleObjectsReturned):
            continue
        else:
            photo.instance_id = instance.id
            photo.save()
