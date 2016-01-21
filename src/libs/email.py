from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader, Context, RequestContext
from django.core.mail import send_mail, BadHeaderError


def send(request, recievers, subject, template, context=None):
    """
        Отправка получателям отрендеренного шаблона.

        Параметр subject поддерживает метку {domain}.
        Также, переменная domain передается в шаблон.

        Функция возвращает True / False.

        Пример:
            send(request, ('reciever1@ya.ru', 'reciever2@ya.ru'),
                subject=_('Message from {domain}'),
                template='module/mails/email.html',
                context={
                    'data': form.cleaned_data,
                }
            )
    """
    if not recievers:
        return True

    if not isinstance(context, Context):
        context = RequestContext(request, context)

    # Добавляем в контекст текущий домен
    site = get_current_site(request)
    context['domain'] = site.domain

    subject = subject.format(domain=site.domain)
    message = loader.get_template(template).render(context)

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
            recipient_list=recievers,
            html_message=message
        )
    except BadHeaderError:
        return False

    return True
