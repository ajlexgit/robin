from django.db import models
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from attachable_blocks.models import AttachableBlock


class ContactsConfig(SingletonModel):
    """ Главная страница """
    header = models.CharField(_('header'), max_length=128)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('contacts:index')

    def __str__(self):
        return self.header


class MessageReciever(models.Model):
    """ Получатели писем с информацией о отправленных сообщениях """
    config = models.ForeignKey(ContactsConfig, related_name='recievers')
    email = models.EmailField(_('e-mail'))

    class Meta:
        verbose_name = _('message reciever')
        verbose_name_plural = _('message recievers')

    def __str__(self):
        return self.email


class Message(models.Model):
    """ Сообщение """
    name = models.CharField(_('name'), max_length=128)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    email = models.EmailField(_('e-mail'), blank=True)
    message = models.TextField(_('message'), max_length=1536)
    date = models.DateTimeField(_('date'), default=now, editable=False)
    referer = models.CharField(_('referer'), max_length=255, blank=True, editable=False)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ('-date',)

    def __str__(self):
        return self.name


class ContactBlock(AttachableBlock):
    """ Подключаемый блок с контактной формой """
    BLOCK_VIEW = 'contacts.views.contact_block_render'

    header = models.CharField(_('header'), max_length=128, blank=True)

    class Meta:
        verbose_name = _('Contact block')
        verbose_name_plural = _('Contact blocks')

    def __str__(self):
        return '%s (Contact Block)' % self.header
