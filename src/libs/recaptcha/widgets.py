from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt


class ReCaptchaWidget(forms.Widget):
    theme = None
    callback = None
    
    class Media:
        js = (
            'recaptcha/js/recaptcha.js',
        )

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)

        final_attrs['data-sitekey'] = settings.RECAPTCHA_PUBLIC_KEY

        final_attrs['data-theme'] = self.theme or \
            getattr(settings, 'RECAPTCHA_DEFAULT_THEME', 'light')

        final_attrs['data-callback'] = self.callback or \
            getattr(settings, 'RECAPTCHA_DEFAULT_CALLBACK', '')

        return mark_safe(
            '<div class="g-recaptcha" {}></div>'.format(flatatt(final_attrs))
        )

    def value_from_datadict(self, data, files, name):
        return data.get('g-recaptcha-response', None)
