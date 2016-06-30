from django.conf import settings


# Конфигурация CKEditorField по умолчанию
CKEDITOR_CONFIG_DEFAULT = {
    'extraPlugins': 'textlen,enterfix',
    'contentsCss': (
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,700,700italic',
        settings.STATIC_URL + 'ckeditor/admin/css/ckeditor.css',
    ),
    'toolbar': [
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']
        },
        {
            'name': 'paragraph',
            'items': ['BulletedList', 'NumberedList']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink', 'Styles', 'Format']
        },
        {
            'name': 'document',
            'items': ['Source']
        },
    ]
}

CKEDITOR_UPLOAD_CONFIG_DEFAULT = {
    'extraPlugins': 'textlen,enterfix,pagephotos,pagevideos,pagefiles,simplephotos',
    'contentsCss': (
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,700,700italic',
        settings.STATIC_URL + 'ckeditor/admin/css/ckeditor.css',
    ),
    'toolbar': [
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']
        },
        {
            'name': 'paragraph',
            'items': ['BulletedList', 'NumberedList', 'Format']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'insert',
            'items': ['PagePhotos', 'PageVideos', 'PageFiles']
        },
        {
            'name': 'document',
            'items': ['Source']
        },
    ]
}
