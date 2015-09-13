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

    def render(self, name, value, attrs=None):
        if value:
            value = self.queryset.get(pk=value)

        gallery_model = self.queryset.model

        # Форматируем аспекты
        aspects = format_aspects(gallery_model.IMAGE_MODEL.ASPECTS, gallery_model.IMAGE_MODEL.VARIATIONS)
        aspects = '|'.join(aspects)

        context = dict(
            name = name,
            gallery = value,
            gallery_model = gallery_model,
            app_label = gallery_model._meta.app_label,
            model_name = gallery_model._meta.model_name,

            aspects = aspects,
            admin_variation = gallery_model.IMAGE_MODEL.get_admin_variation(),
            min_dimensions = gallery_model.IMAGE_MODEL.MIN_DIMENSIONS,
            max_dimensions = gallery_model.IMAGE_MODEL.MAX_DIMENSIONS,
            max_size = gallery_model.IMAGE_MODEL.MAX_SIZE,
        )

        # Ресайз на клиентской стороне
        if gallery_model.IMAGE_MODEL.ADMIN_CLIENT_RESIZE:
            context['max_source'] = gallery_model.IMAGE_MODEL.MAX_SOURCE_DIMENSIONS

        return mark_safe(render_to_string(gallery_model.ADMIN_TEMPLATE, context))
