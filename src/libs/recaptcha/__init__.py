from .fields import ReCaptchaFormField

"""
Поле формы для капчи ReCaptcha 2.0

Docs:
    https://developers.google.com/recaptcha/docs/start


Необходимо подключить скрипт:
    <script src="https://www.google.com/recaptcha/api.js?onload=recaptchaLoadCallback&render=explicit" async defer></script>

Необходимо получить ключи для капчи:
    https://www.google.com/recaptcha/admin#list.
Полученные ключи добавить в settings.py:
    RECAPTCHA_PUBLIC_KEY = '6LfnuwATAAAAAOHTycEayB8UYkz-jN9zr_knTjJZ'
    RECAPTCHA_PRIVATE_KEY = '6LfnuwATAAAAAK9mABR7QIC63sWK0N6wnN2VFiR_'


Необязательные параметры:
    RECAPTCHA_DEFAULT_THEME = 'light'   # или 'dark'
    RECAPTCHA_DEFAULT_CALLBACK = ''     # JS-функция, вызываемая после
                                        # успешного прохождения капчи
    RECAPTCHA_DEFAULT_ERRORS = {}       # Тексты ошибок валидации


Пример использования:
    from libs.recaptcha import ReCaptchaFormField

    class MyForm(forms.Form):
        ...
        captcha = ReCaptchaFormField(theme='dark', callback='myFunc')


Если капча добавляется динамически, то необходимо инициализировать её через JS:
    window.initReCaptcha(element)
"""
