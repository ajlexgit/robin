from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class ContactsConfig(SingletonModel):
    header = models.CharField(_('header'), max_length=128)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('contacts')


class MessageReciever(models.Model):
    config = models.ForeignKey(ContactsConfig, related_name='recievers')
    email = models.EmailField(_('e-mail'))

    class Meta:
        verbose_name = _('message reciever')
        verbose_name_plural = _('message recievers')

    def __str__(self):
        return self.email
