"""
    CKEditorUploadField - поле ckeditor с возможностью закачки картинок.
    CKEditorField - стандартное поле ckeditor.

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

            CKEDITOR_CONFIG_MINI = {
                'lang': 'ru',
                'height': 100,
                'forcePasteAsPlainText': True,
                'extraPlugins': 'autogrow,textlen,enterfix',
                'autoGrow_maxHeight': '500',
                'contentsCss': (STATIC_URL + 'ckeditor/css/ckeditor.css', ),
                'plugins': 'basicstyles,contextmenu,'
                           'elementspath,enterkey,entities,floatingspace,'
                           'format,htmlwriter,justify,link,'
                           'removeformat,resize,showborders,sourcearea,'
                           'tab,toolbar,wsc,wysiwygarea',
                'removeButtons': 'Anchor,Strike,Superscript,Subscript,JustifyBlock',
                'toolbar': [
                    {
                        'name': 'document',
                        'items': ['Source']
                    },
                    {
                        'name': 'links',
                        'items': ['Link', 'Unlink']
                    },
                    {
                        'name': 'basicstyles',
                        'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']
                    },
                    {
                        'name': 'paragraph',
                        'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight']
                    },
                    {
                        'name': 'styles',
                        'items': ['Format']
                    },
                ]
            }

        urls.py:
            ...
            url(r'^ckeditor/', include('ckeditor.urls', namespace='ckeditor')),
            ...


        Пример использования:
            models.py:
                from ckeditor import CKEditorUploadField

                class MyModel(models.Model):
                    ...
                    text = CKEditorUploadField('текст', editor_options=settings.CKEDITOR_CONFIG_MINI)
                    ...

"""
from .fields import CKEditorField, CKEditorUploadField

__all__ = ['CKEditorField', 'CKEditorUploadField']

default_app_config = 'ckeditor.apps.Config'
