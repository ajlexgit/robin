from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from yandex_maps import YandexCoordsField
from google_maps import GoogleCoordsField
from solo.models import SingletonModel


class MainPageConfig(SingletonModel):
    header_title = models.CharField('title', max_length=255)
    address = models.CharField(_('address'), max_length=255, blank=True)
    coords = YandexCoordsField(_('coordinates'), null=True, blank=True)
    coords2 = GoogleCoordsField(_('coordinates'), null=True, blank=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)
    
    class Meta:
        verbose_name = _("Settings")

    def get_absolute_url(self):
        return resolve_url('index')