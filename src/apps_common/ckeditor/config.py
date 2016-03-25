from django.conf import settings


# Конфигурация CKEditorField по умолчанию
CKEDITOR_CONFIG_DEFAULT = {
    'height': 100,
    'forcePasteAsPlainText': True,
    'extraPlugins': 'autogrow,textlen,enterfix',
    'autoGrow_maxHeight': '500',
    'contentsCss': (
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,700,700italic',
        settings.STATIC_URL + 'ckeditor/css/ckeditor.css',
    ),
    'plugins': 'basicstyles,contextmenu,'
               'elementspath,enterkey,entities,floatingspace,'
               'htmlwriter,link,pastefromword,pastetext,'
               'removeformat,resize,showborders,sourcearea,'
               'tab,toolbar,wysiwygarea',
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
    ]
}

CKEDITOR_UPLOAD_CONFIG_DEFAULT = {
    'height': 320,
    'forcePasteAsPlainText': True,
    'extraPlugins': 'autogrow,textlen,enterfix,pagephotos,pagevideos,pagefiles,simplephotos',
    'autoGrow_maxHeight': '540',
    'contentsCss': (
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400italic,700,700italic',
        settings.STATIC_URL + 'ckeditor/css/ckeditor.css',
    ),
    'plugins': 'basicstyles,undo,contextmenu,'
               'elementspath,enterkey,entities,floatingspace,'
               'format,htmlwriter,justify,link,list,liststyle,'
               'removeformat,resize,'
               'showborders,sourcearea,tab,'
               'toolbar,wysiwygarea',
    'removeButtons': 'Anchor,Strike,Superscript,Subscript,JustifyBlock',
    'toolbar': [
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']
        },
        {
            'name': 'paragraph',
            'items': ['NumberedList', 'BulletedList', '-',
                      'JustifyLeft', 'JustifyCenter', 'JustifyRight']
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
            'name': 'styles',
            'items': ['Format']
        },
        {
            'name': 'document',
            'items': ['Source']
        },
    ]
}
