from django.db import models
from django.utils.translation import ugettext_lazy as _
from .api import geocode, DEFAULT
from .fields import GoogleCoords


class MapAndAddress(models.Model):
    address = models.CharField(_('address'), max_length=255, db_index=True)
    longitude = models.FloatField(_('longitude'))
    latitude = models.FloatField(_('latitude'))

    def save(self, *args, **kwargs):
        # Определяет координаты, если они не определены или редактирование
        if self.pk or (self.longitude is None) or (self.latitude is None):
            coords = geocode(self.address)
            if coords:
                self.longitude, self.latitude = coords
        super(MapAndAddress, self).save(*args, **kwargs)

    def __str__(self):
        return self.address


def geocode_cached(address):
    """
    Возвращает кортеж координат (longtitude, latitude,) по строке адреса
    или экземпляру GoogleCoords из БД.
    Если записи в БД нет - определит координаты и сохранит результат в БД.
    """
    if isinstance(address, GoogleCoords):
        return address.lng, address.lat if address else DEFAULT

    # Определяем координаты по адресу
    instance, created = MapAndAddress.objects.get_or_create(address=address)

    if instance.longitude is not None and instance.latitude is not None:
        return instance.longitude, instance.latitude
    else:
        return DEFAULT
