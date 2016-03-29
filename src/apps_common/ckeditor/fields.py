from django.db import models
from django.core import checks
from django.db.models import signals
from django.utils.encoding import smart_text
from .signals.handlers import delete_photos, save_photos
from .forms import CKEditorFormField, CKEditorUploadFormField
from . import config


class CKEditorField(models.Field):
    """ Текстовое поле с WISYWIG редактором """
    def __init__(self, *args, editor_options=None, height=400, **kwargs):
        self.editor_options = editor_options or config.CKEDITOR_CONFIG_DEFAULT
        self.editor_options['height'] = int(height)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_options(**kwargs))
        return errors

    def _check_options(self, **kwargs):
        if not self.editor_options:
            return [
                checks.Error(
                    'options required',
                    obj=self
                )
            ]
        elif not isinstance(self.editor_options, dict):
            return [
                checks.Error(
                    'options must be a dict',
                    obj=self
                )
            ]
        else:
            return []

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
    def __init__(self, *args, editor_options=None, height=540, upload_pagephoto_url='',
            upload_pagefile_url='', upload_simplephoto_url='', **kwargs):
        self.editor_options = editor_options or config.CKEDITOR_UPLOAD_CONFIG_DEFAULT
        self.editor_options['height'] = int(height)
        self.upload_pagephoto_url = upload_pagephoto_url or '/dladmin/ckeditor/upload_pagephoto/'
        self.upload_pagefile_url = upload_pagefile_url or '/dladmin/ckeditor/upload_pagefile/'
        self.upload_simplephoto_url = upload_simplephoto_url or '/dladmin/ckeditor/upload_simplephoto/'
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_options(**kwargs))
        return errors

    def _check_options(self, **kwargs):
        if not self.editor_options:
            return [
                checks.Error(
                    'options required',
                    obj=self
                )
            ]
        elif not isinstance(self.editor_options, dict):
            return [
                checks.Error(
                    'options must be a dict',
                    obj=self
                )
            ]
        else:
            return []

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
            'upload_pagefile_url': self.upload_pagefile_url,
            'upload_simplephoto_url': self.upload_simplephoto_url,
            'model': self.model,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def pre_save(self, model_instance, add):
        """ Сохраняем текст в базу, а картинки - в экземпляр сущности """
        model_instance._page_photos = ()
        model_instance._page_files = ()
        model_instance._simple_photos = ()

        value = self.value_from_object(model_instance)
        if isinstance(value, (list, tuple)):
            if len(value) == 4:
                model_instance._page_photos = value[1].split(',') if value[1] else ()
                model_instance._page_files = value[2].split(',') if value[2] else ()
                model_instance._simple_photos = value[3].split(',') if value[3] else ()
            return value[0]
        return value

    def contribute_to_class(self, cls, name, virtual_only=False):
        super().contribute_to_class(cls, name, virtual_only)
        signals.post_save.connect(save_photos, sender=cls)
        signals.pre_delete.connect(delete_photos, sender=cls)
