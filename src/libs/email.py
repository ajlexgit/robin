import re
from django.conf import settings
from django.template import loader
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags

re_newline_spaces = re.compile(r'[\r \t]*\n[\r \t]*')
re_newlines = re.compile(r'\n{3,}')


def send(request, receivers, subject, message, fail_silently=True):
    if not receivers:
        return True
    if isinstance(receivers, str):
        receivers = [receivers]

    # Вставка домена в subject
    site = get_current_site(request)
    subject = subject.format(domain=site.domain)

    plain = strip_tags(message)
    plain = re_newline_spaces.sub('\n', plain)
    plain = re_newlines.sub('\n\n', plain)

    send_mail(
        subject=subject,
        message=plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=receivers,
        html_message=message,
        fail_silently=fail_silently,
    )


def send_template(request, receivers, subject, template, context=None, fail_silently=True):
    # Добавляем в контекст текущий домен
    site = get_current_site(request)
    context['domain'] = site.domain

    message = loader.get_template(template).render(context, request)
    send(request, receivers, subject, message, fail_silently=fail_silently)
