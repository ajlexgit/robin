from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from libs.variation_field import *


class GalleryWidget(forms.Widget):

    class Media:
        js = (
            'admin/js/jquery.Jcrop.js',
            'admin/js/canvas_utils.js',
            'admin/js/cropdialog.js',
            'admin/js/plupload/moxie.min.js',
            'admin/js/plupload/plupload.min.js',
            'admin/js/plupload/i18n/%s.js' % (settings.SHORT_LANGUAGE_CODE, ),
            'admin/js/plupload/jquery.ui.plupload/jquery.ui.plupload.min.js',
            'gallery/admin/js/gallery_class.js',
            'gallery/admin/js/jquery.gallery.js',
            'gallery/admin/js/gallery.js',
        )
        css = {
            'all': (
                'admin/css/jcrop/jquery.Jcrop.css',
                'admin/css/cropdialog/cropdialog.css',
                'gallery/admin/css/gallery.css',
                'gallery/admin/css/description_window.css',
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}

    def render(self, name, value, attrs=None):
        if value:
            value = self.queryset.get(pk=value)

        gallery_model = self.queryset.model

        context = dict(self.context, **{
            'name': name,
            'gallery': value,
        })
        return mark_safe(render_to_string(gallery_model.ADMIN_TEMPLATE, context))
