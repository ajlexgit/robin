from django.conf import settings


# Конфигурация CKEditorField по умолчанию
CKEDITOR_CONFIG_DEFAULT = {
    'height': 200,
    'extraPlugins': 'textlen,enterfix',
    'contentsCss': (
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,700,700italic',
        settings.STATIC_URL + 'ckeditor/css/ckeditor.css',
    ),
    'toolbar': [
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'document',
            'items': ['Source']
        },
    ]
}

CKEDITOR_UPLOAD_CONFIG_DEFAULT = {
    'height': 540,
    'extraPlugins': 'textlen,enterfix,pagephotos,'
                    'pagevideos,pagefiles,simplephotos',
    'contentsCss': (
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,700,700italic',
        settings.STATIC_URL + 'ckeditor/css/ckeditor.css',
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
        '/',
        {
            'name': 'insert',
            'items': ['PagePhotos', 'PageVideos', 'PageFiles']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'document',
            'items': ['Source']
        },
    ]
}
