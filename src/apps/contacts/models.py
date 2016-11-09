from django.db import models
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from attachable_blocks.models import AttachableBlock
from google_maps.fields import GoogleCoordsField


class ContactsConfig(SingletonModel):
    """ Главная страница """
    header = models.CharField(_('header'), max_length=128)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        default_permissions = ('change', )
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('contacts:index')

    def __str__(self):
        return self.header


class Address(models.Model):
    """ Адрес """
    city = models.CharField(_('city'), max_length=255)
    address = models.CharField(_('address'), max_length=255)
    region = models.CharField(_('region'), max_length=64, blank=True)
    zip = models.CharField(_('zip'), max_length=32, blank=True)
    coords = GoogleCoordsField(_('coords'), blank=True)

    sort_order = models.PositiveIntegerField(_('sort order'))
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        ordering = ('sort_order', )

    @cached_property
    def phones(self):
        return tuple(PhoneNumber.objects.filter(address_id=self.id).values_list('number', flat=True))

    def __str__(self):
        return ', '.join(filter(bool, (self.city, self.address)))


class PhoneNumber(models.Model):
    address = models.ForeignKey(Address, related_name='+')
    number = models.CharField(_('number'), max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(_('sort order'))

    class Meta:
        verbose_name = _('phone')
        verbose_name_plural = _('phones')
        ordering = ('sort_order',)

    def __str__(self):
        return self.number


class NotificationReceiver(models.Model):
    """ Получатели писем с информацией о отправленных сообщениях """
    config = models.ForeignKey(ContactsConfig, related_name='receivers')
    email = models.EmailField(_('e-mail'))

    class Meta:
        verbose_name = _('notification receiver')
        verbose_name_plural = _('notification receivers')

    def __str__(self):
        return self.email


class Message(models.Model):
    """ Сообщение """
    name = models.CharField(_('name'), max_length=128)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    email = models.EmailField(_('e-mail'), blank=True)
    message = models.TextField(_('message'), max_length=2048)
    date = models.DateTimeField(_('date sent'), default=now, editable=False)
    referer = models.CharField(_('from page'), max_length=255, blank=True, editable=False)

    class Meta:
        default_permissions = ('delete', )
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
