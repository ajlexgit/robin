from django.db import models
from django.db.models import signals
from django.utils.encoding import smart_text
from .models import PagePhoto, SimplePhoto
from .forms import CKEditorFormField, CKEditorUploadFormField


class CKEditorField(models.Field):
    """ Текстовое поле с WISYWIG редактором """
    def __init__(self, *args, editor_options=None, **kwargs):
        self.editor_options = editor_options or {}
        super(CKEditorField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if isinstance(value, str) or value is None:
            return value
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CKEditorFormField,
            'editor_options': self.editor_options,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CKEditorUploadField(models.Field):
    """ Текстовое поле с WISYWIG редактором и возможностью загрузки картинок """
    def __init__(self, *args, editor_options=None, upload_pagephoto_url='', upload_simplephoto_url='', **kwargs):
        self.editor_options = editor_options or {}
        self.upload_pagephoto_url = upload_pagephoto_url or '/ckeditor/upload_pagephoto/'
        self.upload_simplephoto_url = upload_simplephoto_url or '/ckeditor/upload_simplephoto/'
        super(CKEditorUploadField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if isinstance(value, str) or value is None:
            return value
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CKEditorUploadFormField,
            'editor_options': self.editor_options,
            'upload_pagephoto_url': self.upload_pagephoto_url,
            'upload_simplephoto_url': self.upload_simplephoto_url,
            'model': self.model,
        }
        defaults.update(kwargs)
        return super(CKEditorUploadField, self).formfield(**defaults)

    @staticmethod
    def pre_delete(instance=None, **kwargs):
        """ Удаление картинок при удалении сущности """
        photos = PagePhoto.objects.filter(app_name=instance._meta.app_label,
                                          model_name=instance._meta.model_name,
                                          instance_id=instance.id)
        photos.delete()

    def pre_save(self, model_instance, add):
        """ Сохраняем текст в базу, а картинки - в экземпляр сущности """
        model_instance._page_photos = ()
        model_instance._simple_photos = ()

        value = getattr(model_instance, self.attname)
        if isinstance(value, list):
            if len(value) == 3:
                model_instance._page_photos = value[1].split(',') if value[1] else ()
                model_instance._simple_photos = value[2].split(',') if value[2] else ()
            return value[0]
        return value

    @staticmethod
    def post_save(instance=None, **kwargs):
        """ Сохраняем в картинках ID сущности, к которой они привязываются """
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

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(CKEditorUploadField, self).contribute_to_class(cls, name, virtual_only)
        signals.post_save.connect(self.post_save, sender=cls)
        signals.pre_delete.connect(self.pre_delete, sender=cls)
