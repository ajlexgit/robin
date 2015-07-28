from urllib import parse
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from suit_ckeditor.widgets import CKEditorWidget
from . import options


class CKEditorUploadWidget(CKEditorWidget):
    """ Виджет редактора, добавляющий данные для определения модели при загрузке файлов """

    model = None
    upload_pagephoto_url = None
    upload_simplephoto_url = None

    class Media:
        js = CKEditorWidget.Media.js + (
            'admin/js/plupload/moxie.min.js',
            'admin/js/plupload/plupload.min.js',
            'admin/js/plupload/i18n/%s.js' % (settings.SHORT_LANGUAGE_CODE, ),
            'admin/js/plupload/jquery.ui.plupload/jquery.ui.plupload.min.js',
        )
        css = CKEditorWidget.Media.css

    def value_from_datadict(self, data, files, name):
        text = data.get(name, None)
        page_photos = data.get(name + '-page-photos', '')
        simple_photos = data.get(name + '-simple-photos', '')
        return [text, page_photos, simple_photos]

    def render(self, name, value, attrs=None):
        # Формируем урл загрузки файлов
        upload_pagephoto_url_parts = list(parse.urlparse(self.upload_pagephoto_url))
        query = dict(parse.parse_qsl(upload_pagephoto_url_parts[4]))
        query.update({
            'app_label': self.model._meta.app_label,
            'model_name': self.model._meta.model_name,
            'field_name': name,
        })
        upload_pagephoto_url_parts[4] = parse.urlencode(query)
        self.editor_options['PAGEPHOTOS_UPLOAD_URL'] = parse.urlunparse(upload_pagephoto_url_parts)

        # Формируем урл загрузки файлов
        upload_simplephoto_url_parts = list(parse.urlparse(self.upload_simplephoto_url))
        query = dict(parse.parse_qsl(upload_simplephoto_url_parts[4]))
        query.update({
            'app_label': self.model._meta.app_label,
            'model_name': self.model._meta.model_name,
            'field_name': name,
        })
        upload_simplephoto_url_parts[4] = parse.urlencode(query)
        self.editor_options['SIMPLEPHOTOS_UPLOAD_URL'] = parse.urlunparse(upload_simplephoto_url_parts)

        # Шаблон урла окна редактирования изображения
        self.editor_options['PAGEPHOTOS_EDIT_URL'] = resolve_url('admin:ckeditor_pagephoto_change', 1)

        # Размер фото на странице
        self.editor_options['PAGEPHOTOS_PHOTO_SIZE'] = options.PAGE_PHOTOS_SIZE
        self.editor_options['SIMPLEPHOTOS_PHOTO_SIZE'] = options.SIMPLE_PHOTOS_MAX_SIZE

        # Максимальный размер файла
        self.editor_options['PAGEPHOTOS_MAX_FILE_SIZE'] = '10mb'
        self.editor_options['SIMPLEPHOTOS_MAX_FILE_SIZE'] = '10mb'

        # Moxie
        self.editor_options['MOXIE_SWF'] = static('admin/js/plupload/Moxie.swf')
        self.editor_options['MOXIE_XAP'] = static('admin/js/plupload/Moxie.xap')

        # CSS приходится грузить JS-ом из-за переопределения стилей
        self.editor_options['PLUPLOADER_CSS'] = (
            static('admin/css/jquery-ui/jquery-ui.min.css'),
            static('admin/js/plupload/jquery.ui.plupload/css/jquery.ui.plupload.css'),
            static('ckeditor/css/ckupload_fix.css'),
        )

        page_photos = []
        simple_photos = []
        if isinstance(value, (tuple, list)):
            page_photos = value[1].split(',')
            simple_photos = value[2].split(',')
            value = value[0]

        output = mark_safe('<input type="hidden" name="{0}-page-photos" value="{1}">'.format(name, ','.join(page_photos)))
        output += mark_safe('<input type="hidden" name="{0}-simple-photos" value="{1}">'.format(name, ','.join(simple_photos)))
        output += super().render(name, value, attrs)
        return output
