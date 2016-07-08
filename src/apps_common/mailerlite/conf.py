from django.conf import settings

API_URL = 'https://api.mailerlite.com/api/'
API_KEY = getattr(settings, 'MAILERLITE_APIKEY')

HTTPS_ALLOWED = False

CKEDITOR_CONFIG = {
    'extraPlugins': 'textlen,enterfix,pagephotos,simplephotos',
    'contentsCss': (
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,700,700italic',
        settings.STATIC_URL + 'ckeditor/admin/css/ckeditor.css',
    ),
    'format_tags': 'p;h1;h2;h3',
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
