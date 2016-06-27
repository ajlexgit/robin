# TODO: antispam

"""
    Модуль подписки на рассылку.

    Зависит от:
        libs.associative_request
        libs.color_field
        libs.templatetags

    Установка:
        # settings.py:
            INSTALLED_APPS = (
                ...
                'mailerlite',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'mailerlite',
                    'icon': 'icon-envelope',
                    'models': (
                        'Campaign',
                        'Group',
                        'Subscriber',
                        'MailerConfig',
                    )
                },
            }

            MAILERLITE_APIKEY = '438b26c79cbd9acea454a4c1ad5eda05'

        # urls.py:
            ...
            url(r'^mailerlite/', include('mailerlite.urls', namespace='mailerlite')),
            ...


    Использование:
        # views.py:
            from mailerlite import SubscribeForm
            from mailerlite.models import Group

            class IndexView(View):
                def get(self, request, *args, **kwargs):
                    ...
                    return self.render_to_response({
                        subscribe_form': SubscribeForm(initial={
                            'groups': Group.objects.all(),
                        }),
                        ...
                    })

        # template.html:
            {% load form_helper %}

            <form action="" method="post">
              {% render_form subscribe_form %}
              <input type="submit" value="Subscribe" class="btn">
            </form>

"""
from . import api
from .forms import SubscribeForm

__all__ = ['api', 'SubscribeForm']

default_app_config = 'mailerlite.apps.Config'