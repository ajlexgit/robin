from django import forms
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class GalleryWidget(forms.Widget):

    class Media:
        js = (
            'admin/js/jquery.Jcrop.js',
            'admin/js/plupload/plupload.full.min.js',
            'admin/js/plupload/i18n/%s.js' % (settings.SHORT_LANGUAGE_CODE, ),
            'admin/js/jquery.canvas.js',
            'admin/js/cropdialog.js',
            'admin/js/uploader.js',
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
        final_attrs = self.build_attrs(attrs, name=name)

        context = dict(self.context, **{
            'name': name,
            'gallery': value,
            'gallery_model': gallery_model,
            'attrs': flatatt(final_attrs),
        })
        return mark_safe(render_to_string(gallery_model.ADMIN_TEMPLATE, context))
