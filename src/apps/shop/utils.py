from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from .models import EmailReciever


def mail_managers(subject, message_template, message_context=None):
    """ Отправка письма менеджерам магазина """
    mail_recievers = EmailReciever.objects.all().values_list('email', flat=True)
    if not mail_recievers:
        return

    mail_content = render_to_string(message_template, message_context)
    if not mail_content:
        return

    try:
        send_mail(
            subject=subject,
            message=mail_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=mail_recievers,
            html_message=mail_content,
        )
    except BadHeaderError:
        pass
