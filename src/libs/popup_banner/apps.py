from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'libs.popup_banner'
    verbose_name = _('Pop-Up Banners')

    def ready(self):
        from libs.js_storage import JS_STORAGE
        from django.core.urlresolvers import reverse

        JS_STORAGE.update({
            'ajax_popup_banner': reverse('popup_banner:ajax_popup_banner'),
        })
