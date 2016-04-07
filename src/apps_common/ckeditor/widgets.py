import json
from urllib import parse
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils.translation import get_language
from suit_ckeditor.widgets import CKEditorWidget as DefaultWidget


class CKEditorWidget(DefaultWidget):
    class Media:
        extend = True
        css = {
            'all': (
                'ckeditor/admin/css/widget.css',
            )
        }
        js = (
            'ckeditor/admin/js/widget.js',
        )

    def render(self, name, value, attrs=None):
        self.editor_options.setdefault('language', get_language())

        attrs = attrs or {}
        attrs.setdefault('class', '')
        attrs['class'] += ' ckeditor-field'
        output = super(DefaultWidget, self).render(name, value, attrs)

        output += mark_safe('''
            <script type="text/javascript">
                window._ckeditor_confs = window._ckeditor_confs || {};
                window._ckeditor_confs["%s"] = %s;
            </script>
        ''' % (name, json.dumps(self.editor_options)))

        return output


class CKEditorUploadWidget(CKEditorWidget):
    """ Виджет редактора, добавляющий данные для определения модели при загрузке файлов """

    model = None
    upload_pagephoto_url = None
    upload_pagefile_url = None
    upload_simplephoto_url = None

    class Media:
        extend = True
        js = (
            'common/js/plupload/plupload.full.min.js',
            'common/js/plupload/jquery.ui.plupload.js',
            'common/js/plupload/i18n/%s.js' % (get_language(), ),
        )

    def value_from_datadict(self, data, files, name):
        text = data.get(name, None)
        page_photos = data.get(name + '-page-photos', '')
        page_files = data.get(name + '-page-files', '')
        simple_photos = data.get(name + '-simple-photos', '')
        return [text, page_photos, page_files, simple_photos]

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
        upload_pagefile_url_parts = list(parse.urlparse(self.upload_pagefile_url))
        query = dict(parse.parse_qsl(upload_pagefile_url_parts[4]))
        query.update({
            'app_label': self.model._meta.app_label,
            'model_name': self.model._meta.model_name,
            'field_name': name,
        })
        upload_pagefile_url_parts[4] = parse.urlencode(query)
        self.editor_options['PAGEFILES_UPLOAD_URL'] = parse.urlunparse(upload_pagefile_url_parts)

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
        self.editor_options['PAGEFILES_EDIT_URL'] = resolve_url('admin:ckeditor_pagefile_change', 1)

        # Размер фото на странице
        self.editor_options['PAGEPHOTOS_THUMB_SIZE'] = (192, 108)

        # Максимальный размер файла
        self.editor_options['PAGEPHOTOS_MAX_FILE_SIZE'] = '10mb'
        self.editor_options['PAGEFILES_MAX_FILE_SIZE'] = '40mb'
        self.editor_options['SIMPLEPHOTOS_MAX_FILE_SIZE'] = '10mb'

        # Moxie
        self.editor_options['MOXIE_SWF'] = static('common/js/plupload/Moxie.swf')
        self.editor_options['MOXIE_XAP'] = static('common/js/plupload/Moxie.xap')

        # CSS приходится грузить JS-ом из-за переопределения стилей
        self.editor_options['PLUPLOADER_CSS'] = (
            static('admin/css/jquery-ui/jquery-ui.min.css'),
            static('common/js/plupload/css/jquery.ui.plupload.css'),
            static('ckeditor/admin/css/ckupload_fix.css'),
        )

        # Youtube APIKEY
        youtube_key = getattr(settings, 'YOUTUBE_APIKEY', 'AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg')
        self.editor_options['YOUTUBE_APIKEY'] = youtube_key

        page_photos = []
        page_files = []
        simple_photos = []
        if isinstance(value, (tuple, list)):
            page_photos = value[1].split(',')
            page_files = value[1].split(',')
            simple_photos = value[2].split(',')
            value = value[0]

        output = mark_safe('<input type="hidden" name="{0}-page-photos" value="{1}">'.format(name, ','.join(page_photos)))
        output += mark_safe('<input type="hidden" name="{0}-page-files" value="{1}">'.format(name, ','.join(page_files)))
        output += mark_safe('<input type="hidden" name="{0}-simple-photos" value="{1}">'.format(name, ','.join(simple_photos)))
        output += super().render(name, value, attrs)
        return output
