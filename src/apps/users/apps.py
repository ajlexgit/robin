from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'users'
    verbose_name = _('Users')
    
    def ready(self):
        from django.shortcuts import resolve_url
        from django.templatetags.static import static
        from libs.js_storage import JS_STORAGE
        
        JS_STORAGE.update({
            'ajax_login': resolve_url('users:ajax_login'),
            'ajax_logout': resolve_url('users:ajax_logout'),
            'ajax_register': resolve_url('users:ajax_register'),
            'ajax_reset': resolve_url('users:ajax_reset'),
            'plupload_moxie_swf': static('js/plupload/Moxie.swf'),
            'plupload_moxie_xap': static('js/plupload/Moxie.xap'),
        })
        