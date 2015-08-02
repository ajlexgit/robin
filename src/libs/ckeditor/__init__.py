from .fields import CKEditorField, CKEditorUploadField

"""
CKEditorUploadField - поле ckeditor с возможностью закачки картинок.
CKEditorField - стандартное поле ckeditor.

Можно поставить на крон удаление картинок, которые не привязаны к сущности
pm clean_page_photos

Установка:
    settings.py:
        INSTALLED_APPS = (
            ...
            'suit_ckeditor',
            'libs.ckeditor',
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
        url(r'^ckeditor/', include('libs.ckeditor.urls', namespace='ckeditor')),
        ...


    Пример использования:
        models.py:
            from libs.ckeditor import CKEditorUploadField

            class MyModel(models.Model):
                ...
                text = CKEditorUploadField('текст', editor_options=settings.CKEDITOR_CONFIG_MINI)
                ...

"""
