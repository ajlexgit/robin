from django.conf import settings


CKEDITOR_DEFAULT_CSS = (
    'https://fonts.googleapis.com/css?family=Roboto:400,400italic,700,700italic',
    settings.STATIC_URL + 'ckeditor/admin/css/ckeditor.css',
)


# Конфигурация CKEditorField по умолчанию
CKEDITOR_CONFIG_DEFAULT = {
    'extraPlugins': 'textlen,enterfix,image_attrs',
    'toolbar': [
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', '-', 'RemoveFormat']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'paragraph',
            'items': ['BulletedList', 'NumberedList']
        },
        {
            'name': 'document',
            'items': ['Styles', 'Format', 'Source']
        },
    ]
}

CKEDITOR_UPLOAD_CONFIG_DEFAULT = {
    'extraPlugins': 'textlen,enterfix,image_attrs,pagephotos,pagevideos,pagefiles,simplephotos,columns,div',
    'toolbar': [
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', '-', 'RemoveFormat']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'paragraph',
            'items': ['BulletedList', 'NumberedList', '-', 'Indent', 'Outdent']
        },
        {
            'name': 'insert',
            'items': ['PagePhotos', 'PageVideos', 'PageFiles', '-', 'Columns', 'Div']
        },
        '/',
        {
            'name': 'document',
            'items': ['Styles', 'Format', 'Source']
        },
    ]
}
