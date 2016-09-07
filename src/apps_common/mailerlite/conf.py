# При конвертации ссылок для Mailerlite вставлять "https://" вместо "http://"
HTTPS_ALLOWED = False

CKEDITOR_CONFIG = {
    'extraPlugins': 'textlen,enterfix,pagephotos,simplephotos',
    'format_tags': 'p;h1;h2',
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
            'items': ['Link', 'Unlink']
        },
        {
            'name': 'insert',
            'items': ['PagePhotos']
        },
        {
            'name': 'document',
            'items': ['Format', 'Source']
        },
    ]
}
