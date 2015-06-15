from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class Config(SingletonModel):
    email = models.EmailField(_('email'), max_length=255, blank=True)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    social_facebook = models.URLField(_('facebook'), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Configuration")
