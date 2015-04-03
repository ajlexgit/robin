import json
from urllib import request, parse
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from .widgets import ReCaptchaWidget

RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'


class ReCaptchaFormField(forms.Field):
    widget = ReCaptchaWidget
    default_error_messages = {
        'response-error': 'Невозможно проверить капчу',
        'missing-input-secret': 'Не указан секретный ключ',
        'invalid-input-secret': 'Секретный ключ неверен',
        'missing-input-response': 'Проверка не пройдена',
        'invalid-input-response': 'Данные некорректны',
    }

    def __init__(self, *args, theme=None, callback=None, **kwargs):
        """
            theme: str      - скин капчи (dark/ligth)
            callback: str   - JS-функция, вызываемая после прохождения капчи
        """
        super().__init__(*args, **kwargs)
        self.widget.theme = theme
        self.widget.callback = callback

        errors = getattr(settings, 'RECAPTCHA_DEFAULT_ERRORS', {})
        self.error_messages.update(errors)

    def validate(self, value):
        qs = parse.urlencode({
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': value,
            'remoteip': '',
        })

        url = '{0}?{1}'.format(RECAPTCHA_URL, qs)
        response = request.urlopen(url)

        if response.code == 200:
            result = json.loads(response.read().decode())
            if not result.get('success'):
                first_error = result.get('error-codes')
                if first_error:
                    raise ValidationError(
                        self.error_messages[first_error[0]],
                        code=first_error[0],
                    )
                else:
                    raise ValidationError(
                        self.error_messages['invalid-input-response'],
                        code='invalid-input-response',
                    )
        else:
            raise ValidationError(
                self.error_messages['response-error'],
                code='response-error'
            )
