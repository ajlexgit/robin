from django.conf import settings
from django.template import loader
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site


def send(request, receivers, subject, template, context=None):
    """
        Отправка получателям отрендеренного шаблона.

        Параметр subject поддерживает метку {domain}.
        Также, переменная domain передается в шаблон.

        Функция возвращает True / False.

        Пример:
            send(request, ('receiver1@ya.ru', 'receiver2@ya.ru'),
                subject=_('Message from {domain}'),
                template='module/mails/email.html',
                context={
                    'data': form.cleaned_data,
                }
            )
    """
    if not receivers:
        return True

    # Добавляем в контекст текущий домен
    site = get_current_site(request)
    context['domain'] = site.domain

    subject = subject.format(domain=site.domain)
    message = loader.get_template(template).render(context, request)

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
            recipient_list=receivers,
            html_message=message
        )
    except BadHeaderError:
        return False

    return True
