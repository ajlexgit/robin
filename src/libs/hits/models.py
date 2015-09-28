from datetime import datetime
from django.db import models
from django.db.models.functions import Coalesce, Value
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

__all__ = ['Hits']


class Hits(models.Model):
    """ Модель счетчика по датам """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    name = models.CharField(_('type'), max_length=64, default='undefined')
    hits = models.PositiveIntegerField(_('hits'), default=0)
    date = models.DateField(_('date'))

    class Meta:
        unique_together = ('content_type', 'object_id', 'name', 'date')

    def __str__(self):
        return '{0}: {1.hits} hits of {1.name!r}'.format(self.date.strftime('%d-%m-%Y'), self)

    @classmethod
    def increment(cls, obj, name='undefined', *, amount=1):
        """ Увеличение значения счетчика """
        ct = ContentType.objects.get_for_model(obj)
        record, created = cls.objects.get_or_create(
            content_type=ct,
            object_id=obj.pk,
            name=name,
            date=datetime.today(),
        )
        cls.objects.filter(pk=record.pk).update(hits=models.F('hits') + amount)

    @classmethod
    def get(cls, obj, name='undefined', *, since=None, to=None):
        """ Получение суммы значений счетчика за указанный период """
        ct = ContentType.objects.get_for_model(obj)
        query = models.Q(
            content_type=ct,
            object_id=obj.pk,
            name=name,
        )

        if since is None:
            if to is None:
                # since == to == None
                pass
            else:
                # since == None, to != None
                query &= models.Q(date__lte=to)
        elif to is None:
            # since != None, to == None
            query &= models.Q(date__gte=since)
        else:
            # since != None, to != None
            query &= models.Q(date__gte=since, date__lte=to)

        return cls.objects.filter(query).aggregate(
            hits=Coalesce(models.Sum('hits'), Value(0))
        )['hits']

    @classmethod
    def clear(cls, obj, name='undefined'):
        """ Очистка счетчика """
        ct = ContentType.objects.get_for_model(obj)
        cls.objects.filter(
            content_type=ct,
            object_id=obj.pk,
            name=name,
        ).delete()
