from django.db import models #стандартные модели django
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from .models import *
from .models import *

class Subscribes(models.Model):
    email = models.EmailField(_('email'), )
    thirdname = models.CharField(_('thirdname'), max_length=128)
    nua = models.CharField(_('nua'), max_length=128)
    name = models.CharField(_('name'), max_length=128)
    sort_order = models.PositiveIntegerField(_('order'), default=0) #поле должно быть больше или равно нулю

    class Meta:
        default_permissions = ('change', )
        verbose_name = _('Subscribe')
        ordering = ('sort_order', )

    def __str__(self):        #метод возвращающий
        return self.name      #строковое представление модели

class Test(models.Model):
    email = models.EmailField(_('email'), )
    thirdname = models.CharField(_('thirdname'), max_length=128)
    nua = models.CharField(_('nua'), max_length=128)
    name = models.CharField(_('name'), max_length=128)
    sort_order = models.PositiveIntegerField(_('order'), default=0)  # поле должно быть больше или равно нулю

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('Subscribe')
        ordering = ('sort_order',)

    def __str__(self):  # метод возвращающий
        return self.name  # строковое представление модели

#------------------------------------------------
class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'

    sort_order = models.PositiveIntegerField(_('order'), default=0)

    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(max_length=2,
                                      choices=YEAR_IN_SCHOOL_CHOICES,
                                      default=FRESHMAN)

    def is_upperclass(self):
        return self.year_in_school in (self.JUNIOR, self.SENIOR)

    class Meta:
        default_permissions = ('change', )
        verbose_name = _('Student')
        ordering = ('sort_order', )

#--------------------------------------------------

class RobinPageConfig(SingletonModel):
    """ Главная страница """
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:                         #класс основанный на методе/объекте
        default_permissions = ('change', )
        verbose_name = _('settings')

    def get_absolute_url(self):         #метод
        return resolve_url('index')

    def __str__(self):                  #метод
        return ugettext('Home page')


