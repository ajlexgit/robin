"""
    CKEditorField - стандартное поле ckeditor.
    CKEditorUploadField - поле ckeditor с возможностью закачки файлов.

    Зависит от:
        libs.media_storage
        libs.stdimage
        libs.upload

    Можно поставить на крон удаление картинок, которые не привязаны к сущности:
        pm clean_pagephotos

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'suit_ckeditor',
                'ckeditor',
                ...
            )

        urls.py:
            ...
            url(r'^dladmin/ckeditor/', include('ckeditor.admin_urls', namespace='admin_ckeditor')),
            url(r'^ckeditor/', include('ckeditor.urls', namespace='ckeditor')),
            ...


        Пример использования:
            models.py:
                from ckeditor import CKEditorUploadField

                class MyModel(models.Model):
                    ...
                    text = CKEditorUploadField(_('text'))
                    ...

"""
from .fields import CKEditorField, CKEditorUploadField

__all__ = ['CKEditorField', 'CKEditorUploadField']

default_app_config = 'ckeditor.apps.Config'
